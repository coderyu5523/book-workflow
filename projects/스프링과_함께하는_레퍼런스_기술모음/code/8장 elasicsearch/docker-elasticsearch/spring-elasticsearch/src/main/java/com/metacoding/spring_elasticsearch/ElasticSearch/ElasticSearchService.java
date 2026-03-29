package com.metacoding.spring_elasticsearch.ElasticSearch;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.elasticsearch.client.elc.NativeQuery;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.metacoding.spring_elasticsearch.device.DeviceDocument;
import com.metacoding.spring_elasticsearch.device.DeviceEntity;
import com.metacoding.spring_elasticsearch.device.DeviceJpaRepository;
import com.metacoding.spring_elasticsearch.device.DeviceSearchRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ElasticSearchService {

        private final DeviceJpaRepository deviceJpaRepository; // H2 또는 MySQL 등 RDB 저장소
        private final DeviceSearchRepository deviceSearchRepository; // Elasticsearch 저장소
        private final ElasticsearchOperations operations; // NativeQuery 실행용

        /**
         * 검색 기능 (Full-Text Search)
         *
         * 클라이언트에서 keyword를 전달하면 Elasticsearch에서 해당 keyword를 분석하여
         * content 필드에서 일치하는 문서를 검색한다.
         *
         * [핵심 기능]
         * 1. match query 사용 → 분석기(analyzer) 기반 full-text 검색 수행
         * 2. fuzziness("AUTO") → 오타 허용 검색 (예: "갤럭시" → "갈럭시"도 매칭)
         * 3. bool.must / should 구조 중 should 사용 → 여러 조건 중 하나라도 맞으면 결과 반환
         * 4. minimumShouldMatch("1") → should 조건 최소 1개 충족해야 검색 결과로 인정
         * 5. operations.search() → ElasticsearchOperations가 DSL 쿼리를 실제로 실행
         *
         * [검색 흐름]
         * keyword 입력 → Analyzer로 토큰화 → Query DSL 생성 → 역색인(Inverted Index) 검색 →
         * BM25 점수 계산 → 최종 결과 반환
         */
        public List<DeviceEntity> searchAll(String keyword) {

                NativeQuery query = NativeQuery.builder()
                                .withQuery(q -> q
                                                .bool(b -> b

                                                                // should: OR 조건. 여러 match 조건을 넣을 수 있고 하나라도 맞으면 통과.
                                                                .should(s1 -> s1

                                                                                // multiMatch 쿼리: full-text 검색(Analyzer
                                                                                // 적용됨)
                                                                                .multiMatch(m -> m

                                                                                                // 검색할 대상 필드,title 우선순위
                                                                                                // 높음
                                                                                                .fields("title^3",
                                                                                                                "content")

                                                                                                // 사용자가 입력한 검색어
                                                                                                .query(keyword)

                                                                                                // 오타 자동 허용
                                                                                                .fuzziness("AUTO")))
                                                                /**
                                                                 * minimumShouldMatch("1")
                                                                 *
                                                                 * - should 조건이 여러 개일 경우 최소 몇 개가 일치해야 하는지 지정.
                                                                 * - 여기서는 should 조건이 하나뿐이므로 “1개 이상” = 해당 조건 반드시 충족해야
                                                                 * 검색됨.
                                                                 * - 예: should가 3개라면 1, 2, 3 등 자유롭게 조절 가능.
                                                                 */
                                                                .minimumShouldMatch("1")))
                                .build();

                /**
                 * 검색 실행.
                 *
                 * operations.search():
                 * - ElasticsearchOperations는 Spring Data Elasticsearch의 핵심 검색 인터페이스.
                 * - query와 Document 타입(DeviceDocument.class)을 넘기면
                 * ES로 DSL 쿼리를 전송하고 검색 결과(SearchHits)를 반환한다.
                 */
                var deviceHits = operations.search(query, DeviceDocument.class);

                List<Long> ids = deviceHits.stream()
                                .map(hit -> hit.getContent().getId())
                                .toList();

                return deviceJpaRepository.findAllById(ids);
        }

        /**
         * 데이터 저장 기능
         *
         * 1) RDB(H2/MySQL)에 DeviceEntity 저장
         * 2) 저장된 데이터를 기반으로 DeviceDocument 생성
         * 3) Elasticsearch에도 동일 데이터를 저장 (dual write)
         */
        @Transactional
        public DeviceDocument saveDevices(DeviceDocument doc) {

                // 1) RDB 저장
                DeviceEntity entity = DeviceEntity.builder()
                                .title(doc.getTitle())
                                .content(doc.getContent())
                                .build();

                DeviceEntity saved = deviceJpaRepository.save(entity);

                // 2) ES 저장용 Document 생성
                DeviceDocument savedDoc = new DeviceDocument(
                                saved.getId(), // DB와 동일한 PK 사용
                                saved.getTitle(),
                                saved.getContent());

                // 3) ES 저장
                deviceSearchRepository.save(savedDoc);

                return savedDoc;
        }

        @Transactional
        public List<DeviceDocument> saveDeviceList(List<DeviceDocument> docs) {

                List<DeviceDocument> savedList = new ArrayList<>();

                for (DeviceDocument doc : docs) {

                        // RDB 저장
                        DeviceEntity entity = DeviceEntity.builder()
                                        .content(doc.getContent())
                                        .title(doc.getTitle())
                                        .build();

                        DeviceEntity saved = deviceJpaRepository.save(entity);

                        // ES Document 준비
                        DeviceDocument savedDoc = new DeviceDocument(
                                        saved.getId(),
                                        saved.getTitle(),
                                        saved.getContent());

                        // ES 인덱스 저장
                        deviceSearchRepository.save(savedDoc);

                        savedList.add(savedDoc);
                }

                return savedList;
        }
}