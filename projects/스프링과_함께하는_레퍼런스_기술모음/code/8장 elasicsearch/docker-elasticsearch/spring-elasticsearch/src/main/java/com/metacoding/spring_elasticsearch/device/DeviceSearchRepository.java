package com.metacoding.spring_elasticsearch.device;

import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

/**
 * DeviceDocument를 Elasticsearch에 저장·조회하기 위한 Repository.
 * 
 * - ElasticsearchRepository<T, ID>
 * → T: 저장될 Document 클래스(DeviceDocument)
 * → ID: 문서의 식별자(Long)
 * 
 * Spring Data JPA와 동일한 방식으로
 * save(), findById(), search(), delete() 등을 제공한다.
 */
public interface DeviceSearchRepository
                extends ElasticsearchRepository<DeviceDocument, Long> {
}