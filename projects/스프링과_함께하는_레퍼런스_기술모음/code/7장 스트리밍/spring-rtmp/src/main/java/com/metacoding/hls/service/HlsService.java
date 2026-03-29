package com.metacoding.hls.service;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.CompletableFuture;

import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import lombok.extern.slf4j.Slf4j;
import net.bramp.ffmpeg.FFmpeg;
import net.bramp.ffmpeg.FFmpegExecutor;
import net.bramp.ffmpeg.FFprobe;
import net.bramp.ffmpeg.builder.FFmpegBuilder;

/**
 * HlsService 클래스는 업로드된 비디오 파일을 HLS(HLS: HTTP Live Streaming) 포맷으로 변환하고,
 * 변환된 HLS 파일들을 제공하는 역할을 합니다.
 *
 * [HLS 구조]
 * HLS는 비디오를 여러 개의 작은 세그먼트(ts 파일들)와 이를 참조하는 플레이리스트(m3u8 파일)로 분할하여 스트리밍하는 기술입니다.
 * 플레이어는 m3u8 파일을 읽고, 그 안에 있는 ts 세그먼트들을 순차적으로 요청하여 재생합니다.
 *
 * [FFmpeg 역할]
 * FFmpeg는 비디오 인코딩 및 변환을 담당하는 툴입니다.
 * 여기서는 FFmpeg를 이용해 원본 비디오를 720p, 1080p 해상도의 HLS 세그먼트와 플레이리스트로 변환합니다.
 *
 * [디렉토리 구조]
 * - upload/original/: 업로드된 원본 비디오 파일을 저장하는 디렉토리입니다.
 * - upload/hls/720p/: 720p 해상도로 변환된 HLS 파일들이 저장되는 디렉토리입니다.
 * - upload/hls/1080p/: 1080p 해상도로 변환된 HLS 파일들이 저장되는 디렉토리입니다.
 *
 * 각각의 해상도별로 별도의 디렉토리를 두어 관리함으로써, 여러 해상도의 스트림을 동시에 제공할 수 있습니다.
 *
 * [입출력 경로]
 * 원본 파일은 ORIGINAL_DIR에 저장되며, 변환된 HLS 파일들은 각각 CONVERT_DIR_720, CONVERT_DIR_1080에
 * 저장됩니다.
 * 이 경로들은 절대경로로 변환하여 FFmpeg에 전달됩니다.
 *
 * [주의사항]
 * - 디렉토리가 없으면 변환 시 에러가 발생하므로, mkdirs()를 통해 필요한 디렉토리를 미리 생성합니다.
 * - 파일명에 한글이나 특수문자가 포함되면 경로 문제 발생 가능성이 있으므로 주의해야 합니다.
 */
@Service
@Slf4j
public class HlsService {

    // 루트 디렉토리 경로
    private final String ROOT_DIR = System.getProperty("user.dir") + "/upload/";

    // 원본 비디오 파일이 저장되는 디렉토리 경로
    private final String ORIGINAL_DIR = ROOT_DIR + "original/";
    // 720p 해상도 변환 결과가 저장되는 디렉토리 경로
    private final String CONVERT_DIR_720 = ROOT_DIR + "hls/720p/";
    // 1080p 해상도 변환 결과가 저장되는 디렉토리 경로
    private final String CONVERT_DIR_1080 = ROOT_DIR + "hls/1080p/";

    /**
     * 업로드된 MultipartFile을 서버 로컬의 ORIGINAL_DIR 디렉토리에 저장하는 메서드입니다.
     */
    public String saveOriginalVideo(MultipartFile file) throws IOException {

        // ORIGINAL_DIR 경로에 디렉토리가 존재하지 않으면 생성합니다.
        // mkdirs()는 중간 경로가 없으면 모두 생성해줍니다.
        new File(ORIGINAL_DIR).mkdirs();

        // 업로드된 파일의 실제 이름
        // String fileName = file.getOriginalFilename()을 사용하는 것이 원칙이지만,
        // 이 교육용 HLS 서버는 "항상 하나의 최신 영상만 재생"하는 구조이므로
        // 여러 파일명을 관리할 필요가 없습니다.

        // 따라서, 업로드될 때마다 동일한 이름(video.mp4)으로 저장하여
        // 이전 파일을 덮어쓰도록 합니다.
        // String originalName = file.getOriginalFilename();
        // String ext = originalName.substring(originalName.lastIndexOf("."));
        // String fileName = "video" + ext; // video.mp4 / video.mov / video.webm

        String fileName = "video.mp4";
        // ORIGINAL_DIR 경로와 파일명을 합쳐 저장할 File 객체를 생성합니다.
        File saveFile = new File(ORIGINAL_DIR + fileName);

        // MultipartFile의 내용을 saveFile에 실제로 저장합니다.
        file.transferTo(saveFile);

        // 저장된 파일명을 반환합니다.
        return fileName;
    }

    /**
     * 저장된 원본 비디오 파일을 즉시 HLS 포맷으로 변환하는 메서드입니다.
     * 720p, 1080p 두 가지 해상도로 변환하여 각각 별도의 디렉토리에 저장합니다.
     */
    public void convertToHls(String fileName) throws IOException {

        // 원래는 fileName에서 확장자를 제거하여 baseName을 계산해야 합니다.
        // 예: video.mp4 -> video

        // [코드 예시]
        // String baseName = fileName;
        // int dotIndex = baseName.lastIndexOf(".");
        // if (dotIndex != -1)
        // baseName = baseName.substring(0, dotIndex);

        // 이렇게 해야 여러 파일명을 구분하여 각각의 HLS 스트림을 만들 수 있습니다.
        // 하지만 이 프로젝트는 "최신 영상 하나만 HLS로 변환"하는 단일 스트림 서버이므로,
        // HLS 출력 파일명 또한 항상 동일한 이름으로 만들어야
        // 프론트에서 고정된 URL(/hls/720p/video.m3u8)로 재생이 가능합니다.

        // 따라서 baseName을 강제로 "video"로 고정하여
        // video.m3u8, video0.ts, video1.ts … 처럼 항상 같은 이름으로 HLS 출력이 생성되도록 합니다.
        String baseName = "video";

        // 원본 파일의 절대 경로를 생성합니다.
        String inputPath = new File(ORIGINAL_DIR + fileName).getAbsolutePath();

        // 변환 결과를 저장할 720p, 1080p 디렉토리가 없으면 생성합니다.
        new File(CONVERT_DIR_720).mkdirs();
        new File(CONVERT_DIR_1080).mkdirs();

        // 출력 m3u8 플레이리스트 파일의 절대 경로를 생성합니다.
        String output720 = new File(CONVERT_DIR_720, baseName + ".m3u8").getAbsolutePath();
        String output1080 = new File(CONVERT_DIR_1080, baseName + ".m3u8").getAbsolutePath();

        // FFmpeg, FFprobe 객체를 생성합니다.
        // FFprobe는 미디어 파일 정보를 분석하는 데 사용됩니다.
        FFmpeg ffmpeg = new FFmpeg();
        FFprobe ffprobe = new FFprobe();
        // FFmpegExecutor는 빌더로부터 생성된 명령을 실행하는 역할을 합니다.
        FFmpegExecutor executor = new FFmpegExecutor(ffmpeg, ffprobe);

        // 720p 변환을 위한 FFmpegBuilder 설정
        FFmpegBuilder builder720 = new FFmpegBuilder()
                .setInput(inputPath) // 입력 파일 경로 지정
                .addOutput(output720) // 출력 파일 경로 지정 (m3u8)

                // -b:v : 목표 bitrate(평균 bitrate).
                // 영상이 전체적으로 어느 정도의 품질(정보량)로 인코딩될지 결정하는 옵션.
                // 2500k = 2.5Mbps 로, 일반적인 720p 품질에 사용되는 bitrate.
                .addExtraArgs("-b:v", "2500k")

                // -maxrate : 인코더가 순간적으로 사용할 수 있는 최대 bitrate.
                // 움직임이 많은 장면에서 품질이 너무 떨어지지 않도록 상한선을 설정.
                // 여기서는 평균(2500k)과 동일하게 2500k 로 제한.
                .addExtraArgs("-maxrate", "2500k")

                // -bufsize : bitrate 변동 허용 폭(버퍼 크기).
                // maxrate 이 어느 정도까지 출렁거릴지 결정하는 비디오 버퍼링 사이즈.
                // 일반적으로 maxrate 의 2배 설정이 안정적 → 5000k.
                .addExtraArgs("-bufsize", "5000k")
                .addExtraArgs("-vf", "scale=-2:720") // 비디오 필터: 세로 해상도 720, 가로는 비율 유지(-2)
                .addExtraArgs("-profile:v", "baseline") // H.264 baseline 프로파일 사용 (호환성 위해)
                .addExtraArgs("-level", "3.0") // H.264 레벨 설정
                .addExtraArgs("-start_number", "0") // HLS 세그먼트 번호 시작값
                .addExtraArgs("-hls_time", "10") // 각 세그먼트 길이(초)
                .addExtraArgs("-hls_list_size", "0") // 플레이리스트에 모든 세그먼트 포함 (0은 무제한)
                .addExtraArgs("-f", "hls") // 출력 포맷을 HLS로 지정
                .done();

        // 1080p 변환을 위한 FFmpegBuilder 설정 (720p와 옵션 동일, 해상도, bitrate만 다름)
        FFmpegBuilder builder1080 = new FFmpegBuilder()
                .setInput(inputPath)
                .addOutput(output1080)
                .addExtraArgs("-b:v", "5000k")
                .addExtraArgs("-maxrate", "5000k")
                .addExtraArgs("-bufsize", "10000k")
                .addExtraArgs("-vf", "scale=-2:1080")
                .addExtraArgs("-profile:v", "baseline")
                .addExtraArgs("-level", "3.0")
                .addExtraArgs("-start_number", "0")
                .addExtraArgs("-hls_time", "10")
                .addExtraArgs("-hls_list_size", "0")
                .addExtraArgs("-f", "hls")
                .done();

        // 720p 변환 작업 실행
        executor.createJob(builder720).run();
        // 1080p 변환 작업 실행
        executor.createJob(builder1080).run();

        // 변환 완료 로그 출력
        log.info("HLS 변환 완료: {}", fileName);
    }

    /**
     * HLS 변환을 비동기로 실행합니다.
     * 업로드 응답을 빠르게 반환하고, 변환은 백그라운드에서 진행됩니다.
     */
    @Async
    public CompletableFuture<Void> convertToHlsAsync(String fileName) {
        try {
            convertToHls(fileName);
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("HLS 비동기 변환 실패: {}", fileName, e);
            return CompletableFuture.failedFuture(e);
        }
    }

    /**
     * 클라이언트(브라우저 또는 Hls.js)가 요청하는 ts 세그먼트 또는 m3u8 플레이리스트 파일을 반환합니다.
     *
     * Hls.js는 m3u8 플레이리스트를 읽고, 플레이리스트 내에 명시된 ts 세그먼트 파일들을 순차적으로 요청합니다.
     * 따라서 이 메서드는 요청된 해상도(quality)와 파일명에 맞는 파일을 찾아 Resource로 반환합니다.
     */
    public Resource loadHlsFile(String quality, String fileName) throws IOException {

        String path;

        // 요청된 해상도에 따라 해당 디렉토리 경로를 지정합니다.
        if (quality.equals("720p"))
            path = CONVERT_DIR_720;
        else if (quality.equals("1080p"))
            path = CONVERT_DIR_1080;
        else
            throw new RuntimeException("지원하지 않는 해상도");

        // 요청된 파일명을 포함한 실제 파일 객체 생성
        File file = new File(path, fileName);
        // 파일이 존재하지 않으면 IOException 발생
        if (!file.exists())
            throw new IOException("파일 없음: " + file.getAbsolutePath());

        /*
         * Hls.js가 ts 세그먼트나 m3u8 파일을 요청할 때,
         * 파일 시스템의 절대 경로를 정확히 전달해야 하므로 getCanonicalPath()를 사용합니다.
         * 이는 심볼릭 링크나 상대 경로 문제를 해결하여 정확한 경로를 반환합니다.
         */
        return new FileSystemResource(file.getCanonicalPath());
    }
}