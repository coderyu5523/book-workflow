package com.metacoding.hls.controller;

import java.io.IOException;

import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.metacoding.hls.service.HlsService;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@RestController
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*") // HLS.ts 파일 요청은 브라우저가 자동으로 발생하므로 CORS 허용 필요
public class HlsController {

    private final HlsService hlsService;

    /**
     * 업로드 → 저장 → HLS 변환 요청(비동기) → 즉시 응답
     *
     * 이 엔드포인트는 multipart/form-data 형식의 요청을 받는다.
     *
     * [Postman 설정 방법]
     * - Method : POST
     * - URL : http://localhost:8080/upload
     * - Body : form-data 선택
     * - Key : file
     * - Type : File
     * - Value: 업로드할 영상 파일 선택 (예: streaming.mp4)
     *
     * [전체 흐름]
     * 1) 클라이언트(포스트맨/브라우저)가 form-data 로 비디오 파일을 업로드한다.
     * 2) 스프링이 해당 파일을 MultipartFile 로 매핑한다.
     * 3) saveOriginalVideo() 가 upload/original/ 폴더에 원본 파일을 저장한다.
     * 4) convertToHlsAsync() 가 저장된 파일명을 이용해 FFmpeg 로 HLS(m3u8 + ts) 변환을 시작한다.
     * 5) 변환 요청이 접수되었다는 메시지를 즉시 응답한다.
     */
    @PostMapping("/upload")
    public ResponseEntity<String> uploadVideo(@RequestParam("file") MultipartFile file) throws IOException {

        log.info("업로드 요청 들어옴: {}", file.getOriginalFilename());

        // 1) 업로드된 파일을 디스크에 저장 (예: upload/original/streaming.mp4)
        String savedName = hlsService.saveOriginalVideo(file);

        // 2) 저장된 파일명을 기준으로 720p, 1080p HLS 변환 비동기 실행
        hlsService.convertToHlsAsync(savedName);

        // 3) 클라이언트에게 변환 요청 접수 메시지 반환
        return ResponseEntity.accepted().body("HLS 변환 시작: " + file.getOriginalFilename() + "->" + savedName);
    }

    /**
     * m3u8 파일 제공
     * - HLS.js는 m3u8 파일을 먼저 요청하고, 그 안에 있는 ts 세그먼트 파일을 자동으로 계속 요청함.
     * - 예: /hls/720/video.m3u8
     */
    @GetMapping("/hls/{quality}/{fileName}.m3u8")
    public ResponseEntity<Resource> getHlsPlaylist(
            @PathVariable String quality,
            @PathVariable String fileName) throws IOException {

        // 예: upload/hls/720p/video.m3u8
        Resource resource = hlsService.loadHlsFile(quality, fileName + ".m3u8");

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType("application/vnd.apple.mpegurl"));

        log.info("m3u8 전송: /hls/{}/{}.m3u8", quality, fileName);

        return new ResponseEntity<>(resource, headers, HttpStatus.OK);
    }

    /**
     * TS 세그먼트 파일 제공
     * - m3u8 파일은 여러 개의 ts 세그먼트 목록을 포함한다.
     * - HLS 플레이어는 이 ts 파일들을 자동으로 순차적 다운로드하여 영상 재생을 완성한다.
     *
     * 예:
     * /hls/720/video0.ts
     * /hls/720/video1.ts
     * /hls/720/video2.ts
     */
    @GetMapping("/hls/{quality}/{tsSegment}.ts")
    public ResponseEntity<Resource> getHlsTs(
            @PathVariable String quality,
            @PathVariable String tsSegment) throws IOException {

        // 실제 TS 파일 로드
        Resource resource = hlsService.loadHlsFile(quality, tsSegment + ".ts");

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);

        log.info("TS 전송: /hls/{}/{}.ts", quality, tsSegment);

        return new ResponseEntity<>(resource, headers, HttpStatus.OK);
    }
}
