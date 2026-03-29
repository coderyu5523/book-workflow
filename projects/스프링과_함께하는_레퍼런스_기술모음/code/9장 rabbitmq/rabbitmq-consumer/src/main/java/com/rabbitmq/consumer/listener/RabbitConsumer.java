package com.rabbitmq.consumer.listener;

import com.rabbitmq.consumer.dto.RabbitDTO;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Objects;

@Component
public class RabbitConsumer {

    private static final String README_PATH = "./README.md"; // 프로젝트 루트 기준

    @RabbitListener(queues = "${rabbit.queue}")
    public void receive(RabbitDTO message) {
        System.out.println("=== 메시지 수신 ===");
        System.out.println("Repository: " + message.getRepo());
        System.out.println("SHA: " + message.getSha());
        System.out.println("타임스탬프: " + message.getTimestamp());
        System.out.println("변경 사항을 비교 후 README.md에 패치합니다...");

        try {
            patchFile(message.getContent());
        } catch (IOException e) {
            System.err.println("파일 업데이트 중 오류 발생: " + e.getMessage());
        }
    }

    private void patchFile(String newContent) throws IOException {
        File file = new File(README_PATH);

        // 기존 파일이 없는 경우 새로 생성
        if (!file.exists()) {
            writeContent(file, newContent);
            System.out.println("기존 파일이 없어 새로 생성");
            return;
        }

        // 기존 내용 읽기
        String oldContent = Files.readString(file.toPath(), StandardCharsets.UTF_8);

        // 동일하면 변경하지 않음
        if (Objects.equals(oldContent.trim(), newContent.trim())) {
            System.out.println("변경 사항 없음. 파일 수정 생략.");
            return;
        }

        // 백업 폴더 생성
        File backupDir = new File(file.getParent(), "backups");
        if (!backupDir.exists()) {
            backupDir.mkdirs(); // 폴더가 없으면 생성
        }

        // 백업 파일명: readme_backup_날짜시간.md
        String backupFileName = String.format("readme_backup_%d.md", System.currentTimeMillis());
        File backupFile = new File(backupDir, backupFileName);

        // 백업 파일 저장
        Files.copy(file.toPath(), backupFile.toPath(), java.nio.file.StandardCopyOption.REPLACE_EXISTING);

        System.out.println("백업 파일 생성 완료 → " + backupFile.getAbsolutePath());

        // 새로운 내용 반영
        writeContent(file, newContent);
        System.out.println("변경 사항 감지됨 → readme.md 업데이트 완료 (백업: readme_backup.md)");
    }

    private void writeContent(File file, String content) throws IOException {
        try (Writer writer = new OutputStreamWriter(new FileOutputStream(file, false), StandardCharsets.UTF_8)) {
            writer.write(content);
        }
    }
}