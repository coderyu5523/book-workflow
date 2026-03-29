package com.metacoding.spring_elasticsearch.device;

import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * Elasticsearch에 저장되는 Document 모델.
 *
 * @Document(indexName = "devices")
 *                     → Elasticsearch 인덱스명 지정
 *
 * @Field(type = FieldType.Text)
 *             → content는 full-text 검색을 위해 Text 타입으로 설정
 */
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Document(indexName = "devices")
public class DeviceDocument {

    private Long id; // RDB의 PK와 동일하게 매핑

    // Text 타입 → 단어 분석 및 역색인, full-text 검색에 적합
    @Field(type = FieldType.Text)
    private String title;

    // Text 타입 → 단어 분석 및 역색인, full-text 검색에 적합
    @Field(type = FieldType.Text)
    private String content;
}