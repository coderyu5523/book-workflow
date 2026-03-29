package com.rabbitmq.producer.github;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class GitHubClient {

    @Value("${github.owner}")
    private String owner;

    @Value("${github.repo}")
    private String repo;

    @Value("${github.readme-path}")
    private String readmePath;

    private final RestTemplate restTemplate = new RestTemplate();

    // ✅ 최신 SHA 조회 (제네릭 타입 명시 + null 안전 처리)
    public String fetchLatestSha() {
        String url = String.format(
                "https://api.github.com/repos/%s/%s/commits?path=%s&per_page=1",
                owner, repo, readmePath);

        ResponseEntity<List<Map<String, Object>>> response = restTemplate.exchange(url, HttpMethod.GET, null,
                (Class<List<Map<String, Object>>>) (Class<?>) List.class);

        List<Map<String, Object>> commits = response.getBody();

        if (commits == null || commits.isEmpty()) {
            System.out.println("[GitHubClient] 커밋 목록이 비어 있습니다.");
            return null;
        }

        Map<String, Object> commitObj = commits.get(0);
        Object sha = commitObj.get("sha");
        return sha != null ? sha.toString() : null;
    }

    // ✅ README 원문 가져오기 (SHA 기준)
    public String fetchReadmeContent(String sha) {
        String rawUrl = String.format(
                "https://raw.githubusercontent.com/%s/%s/%s/%s",
                owner, repo, sha, readmePath);
        return restTemplate.getForObject(rawUrl, String.class);
    }

    public String getRepoFullName() {
        return owner + "/" + repo;
    }
}
