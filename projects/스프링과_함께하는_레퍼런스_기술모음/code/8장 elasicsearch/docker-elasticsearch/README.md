# 8장 Elasticsearch 키워드 검색


## 샘플 데이터
```SQL
[
  {
    "title": "갤럭시",
    "content": "갤럭시 S23 기본 모델 빠른 스마트폰 성능"
  },
  {
    "title": "갤럭시",
    "content": "갤럭시 S23 울트라 고급 카메라 성능 우수한 스마트폰"
  },
  {
    "title": "갤럭시",
    "content": "갤럭시 S23 플러스 큰 화면과 배터리 효율 좋은 모델"
  },
  {
    "title": "갤럭시",
    "content": "갤럭시 Z 플립4 접히는 디자인과 휴대성이 뛰어난 스마트폰"
  },
  {
    "title": "갤럭시",
    "content": "갤럭시 Z 플립5 대형 커버 화면과 향상된 촬영 기능"
  },
  {
    "title": "아이폰",
    "content": "아이폰 14 기본 모델 안정적인 성능과 카메라"
  },
  {
    "title": "아이폰",
    "content": "아이폰 14 프로 고급 카메라 기능과 다이내믹 아일랜드 제공"
  },
  {
    "title": "아이폰",
    "content": "아이폰 14 프로 맥스 큰 화면과 최고의 성능"
  },
  {
    "title": "아이폰",
    "content": "아이폰 15 향상된 배터리와 새로운 컬러의 스마트폰"
  },
  {
    "title": "아이폰",
    "content": "아이폰 15 프로 가벼운 티타늄 바디와 높은 퍼포먼스"
  }
]
```


## Kibana Dev Tools 사용법

Kibana에서 **Dev Tools > Console**을 열고 아래 요청을 순서대로 실행합니다.

### 인덱스 상태 확인

```http
HEAD /devices
```

### 인덱스 삭제

```http
DELETE /devices
```

### 인덱스 기본 조회

```http
GET /devices
```

### 매핑 확인

```http
GET /devices/_mapping
```

### 문서 개수 확인

```http
GET /devices/_count
```

### 전체 조회 (match_all)

```http
GET /devices/_search
{
  "query": { "match_all": {} }
}
```

### 특정 문서 조회

```http
GET /devices/_doc/3
```

### 단일 필드 검색 (match)

```http
GET /devices/_search
{
  "query": {
    "match": {
      "title": "갤럭시"
    }
  }
}
```

### 멀티 필드 검색 (multi_match)

```http
GET /devices/_search
{
  "query": {
    "multi_match": {
      "query": "갤럭시",
      "fields": ["title^3", "content"]
    }
  }
}
```

### ID 기반 검색 (term)

```http
GET /devices/_search
{
  "query": {
    "term": {
      "id": 11
    }
  }
}
```

### 문서 직접 저장

```http
POST /devices/_doc
{
  "id": 11,
  "title": "갤럭시 S25",
  "content": "신형 갤럭시 모델"
}
```
