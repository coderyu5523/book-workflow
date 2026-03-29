package com.rabbitmq.producer.scheduler;

import java.time.LocalDateTime;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.rabbitmq.producer.dto.RabbitDTO;
import com.rabbitmq.producer.github.GitHubClient;
import com.rabbitmq.producer.rabbit.RabbitProducer;

import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class PollingScheduler {

    private final GitHubClient gitHubClient;
    private final RabbitProducer rabbitProducer;

    // ✅ 마지막으로 확인한 커밋 해시 저장
    private String lastSha = null;

    // ✅ 30초 마다 실행 (github.poll-interval-ms 설정 기반)
    @Scheduled(fixedRateString = "${github.poll-interval-ms}")
    public void checkForReadmeChange() {
        try {
            // ① 최신 README 커밋 SHA 가져오기
            String latestSha = gitHubClient.fetchLatestSha();
            if (latestSha == null) {
                System.out.println("[폴링] 커밋 SHA를 가져오지 못했습니다.");
                return;
            }

            // ② 이전 SHA와 비교 → 변경 없으면 종료
            if (latestSha.equals(lastSha)) {
                System.out.println("[폴링] 변경 없음 → SHA: " + latestSha);
                return;
            }

            // ③ 변경 감지 시 SHA 갱신
            lastSha = latestSha;
            System.out.println("[폴링] README 변경 감지 → 새로운 SHA: " + latestSha);

            // ④ README 파일 내용(raw.githubusercontent.com) 가져오기
            String content = gitHubClient.fetchReadmeContent(latestSha);

            // ⑤ RabbitMQ로 발행할 DTO 생성
            RabbitDTO message = RabbitDTO.builder()
                    .repo(gitHubClient.getRepoFullName())
                    .sha(latestSha)
                    .content(content)
                    .timestamp(LocalDateTime.now())
                    .build();

            // ⑥ RabbitMQ에 발행
            rabbitProducer.send(message);

        } catch (Exception e) {
            System.err.println("[ERROR] 폴링 중 오류: " + e.getMessage());
        }
    }
}
