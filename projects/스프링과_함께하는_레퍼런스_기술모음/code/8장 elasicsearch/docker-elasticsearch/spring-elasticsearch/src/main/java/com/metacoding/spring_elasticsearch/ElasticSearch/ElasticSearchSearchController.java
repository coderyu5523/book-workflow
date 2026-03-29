package com.metacoding.spring_elasticsearch.ElasticSearch;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.metacoding.spring_elasticsearch.device.DeviceDocument;
import com.metacoding.spring_elasticsearch.device.DeviceEntity;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
public class ElasticSearchSearchController {

    private final ElasticSearchService elasticSearchService;

    @GetMapping("/")
    public String healthCheck() {
        return "엘라스틱서치 스프링 서버 연결 성공";
    }

    /**
     * 단일 Device 저장 API
     * - Body로 { "content": "갤럭시 S23" } 형태 전달
     * - H2 + Elasticsearch dual 저장
     */
    @PostMapping("/device")
    public DeviceDocument saveDevice(@RequestBody DeviceDocument doc) {
        return elasticSearchService.saveDevices(doc);
    }

    // 여러 Device 문서를 한 번에 저장
    @PostMapping("/devices")
    public List<DeviceDocument> saveDevices(@RequestBody List<DeviceDocument> docs) {
        return elasticSearchService.saveDeviceList(docs);
    }

    /**
     * 검색 API
     * - GET /api/search?keyword=갤럭시
     * - Elasticsearch에 full-text 검색 수행
     */
    @GetMapping("/search")
    public List<DeviceEntity> search(@RequestParam("keyword") String keyword) {
        System.out.println(keyword + " :Aaaa"); // 로그
        return elasticSearchService.searchAll(keyword);
    }
}