"""ex08 — Cross-Encoder ReRanker 모듈."""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

console = Console()

# --- 상수 정의 ---
BASE_DIR = Path(__file__).resolve().parent.parent

# Cross-Encoder 모델 (한국어 지원)
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
# 한국어 전용 대안: "bongsoo/moco-cross-encoder-v2"

# 인메모리 샘플 문서 (reranker 실험용)
SAMPLE_DOCUMENTS = [
    {"id": "d01", "content": "연차유급휴가는 1년 이상 근속 직원에게 15일 부여됩니다.", "score": 0.45},
    {"id": "d02", "content": "연차 신청은 3일 전 인사담당자에게 서면 제출해야 합니다.", "score": 0.42},
    {"id": "d03", "content": "팀장은 업무 상황에 따라 휴가 시기를 조정할 수 있습니다.", "score": 0.38},
    {"id": "d04", "content": "재택근무는 입사 6개월 이상 정규직에 한해 신청 가능합니다.", "score": 0.35},
    {"id": "d05", "content": "성과 평가는 목표달성도 60%, 역량평가 30%, 동료평가 10%입니다.", "score": 0.32},
    {"id": "d06", "content": "출장비는 출장 후 5영업일 이내에 영수증과 함께 정산해야 합니다.", "score": 0.28},
    {"id": "d07", "content": "개인 USB 사용은 IT보안팀 승인 없이 금지됩니다.", "score": 0.25},
    {"id": "d08", "content": "자기계발비는 연 50만원 한도로 도서, 강의, 자격증에 사용 가능합니다.", "score": 0.22},
    {"id": "d09", "content": "퇴직금은 근속 1년 이상 시 30일분 평균임금으로 산정합니다.", "score": 0.18},
    {"id": "d10", "content": "육아휴직은 만 8세 이하 자녀가 있는 직원이 최대 1년 신청 가능합니다.", "score": 0.15},
]


class CrossEncoderReranker:
    """Cross-Encoder 기반 리랭커."""

    def __init__(self, model_name=CROSS_ENCODER_MODEL):
        """초기화 및 모델 로드를 수행합니다."""
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Cross-Encoder 모델을 로드합니다."""
        try:
            from sentence_transformers import CrossEncoder

            console.print(f"[dim]Cross-Encoder 모델 로드 중: {self.model_name}[/dim]")
            self.model = CrossEncoder(self.model_name)
            console.print("[green]Cross-Encoder 모델 로드 완료[/green]")

        except ImportError:
            console.print(
                "[red]sentence-transformers 패키지가 설치되지 않았습니다.[/red]"
            )
            console.print("pip install sentence-transformers 를 실행하십시오.")
            sys.exit(1)

        except Exception as e:
            console.print(f"[red]모델 로드 실패: {e}[/red]")
            console.print("[yellow]오프라인 환경이거나 모델 이름을 확인하십시오.[/yellow]")
            raise

    def rerank(self, query, documents, top_k=5):
        """검색 결과를 Cross-Encoder로 재정렬합니다."""
        if self.model is None:
            console.print("[red]모델이 로드되지 않았습니다.[/red]")
            return documents[:top_k]

        # Cross-Encoder에 입력할 쌍(query, document) 생성
        pairs = [(query, doc["content"]) for doc in documents]

        # Cross-Encoder 점수 계산
        scores = self.model.predict(pairs)

        # 점수 부여 및 정렬
        for doc, score in zip(documents, scores):
            doc["cross_encoder_score"] = float(score)

        reranked = sorted(
            documents,
            key=lambda x: x.get("cross_encoder_score", 0),
            reverse=True
        )

        return reranked[:top_k]


class SimpleReranker:
    """Cross-Encoder 없이 동작하는 단순 리랭커."""

    def rerank(self, query, documents, top_k=5):
        """키워드 매칭 기반으로 문서를 재정렬합니다."""
        query_words = set(query.lower().split())

        for doc in documents:
            doc_words = set(doc["content"].lower().split())
            intersection = query_words & doc_words
            # 질문 단어 일치율을 re-rank 점수로 사용
            doc["cross_encoder_score"] = (
                len(intersection) / len(query_words) if query_words else 0.0
            )

        reranked = sorted(
            documents,
            key=lambda x: x.get("cross_encoder_score", 0),
            reverse=True
        )

        return reranked[:top_k]


def create_reranker(use_simple=False):
    """환경에 따라 적절한 리랭커를 생성합니다."""
    if use_simple:
        console.print("[cyan]SimpleReranker (키워드 기반) 사용[/cyan]")
        return SimpleReranker()

    try:
        import sentence_transformers
        return CrossEncoderReranker()
    except ImportError:
        console.print(
            "[yellow]sentence-transformers 없음. SimpleReranker로 대체합니다.[/yellow]"
        )
        return SimpleReranker()


def simulate_initial_retrieval(query, documents, top_k=10):
    """초기 벡터 검색 결과를 시뮬레이션합니다."""
    import copy
    docs = copy.deepcopy(documents)

    # 쿼리 키워드 기반으로 점수 약간 조정 (시뮬레이션)
    query_words = set(query.lower().split())
    for doc in docs:
        doc_words = set(doc["content"].lower().split())
        bonus = 0.05 * len(query_words & doc_words)
        doc["score"] = min(doc["score"] + bonus, 1.0)

    docs.sort(key=lambda x: x["score"], reverse=True)
    return docs[:top_k]


def compare_before_after_reranking(query, initial_results, reranked_results):
    """리랭킹 전후 순위를 비교합니다."""
    comparison = {
        "query": query,
        "before": [],
        "after": []
    }

    for rank, doc in enumerate(initial_results, 1):
        comparison["before"].append({
            "rank": rank,
            "id": doc["id"],
            "score": doc.get("score", 0.0),
            "content_preview": doc["content"][:40] + "..."
        })

    for rank, doc in enumerate(reranked_results, 1):
        comparison["after"].append({
            "rank": rank,
            "id": doc["id"],
            "score": doc.get("cross_encoder_score", 0.0),
            "content_preview": doc["content"][:40] + "..."
        })

    return comparison


def calculate_rank_change(before, after):
    """리랭킹 전후 순위 변화를 계산합니다."""
    before_ranks = {item["id"]: item["rank"] for item in before}
    after_ranks = {item["id"]: item["rank"] for item in after}

    changes = []
    for doc_id, after_rank in after_ranks.items():
        before_rank = before_ranks.get(doc_id, 99)
        change = before_rank - after_rank
        changes.append({
            "문서 ID": doc_id,
            "리랭킹 전 순위": before_rank if before_rank < 99 else "신규",
            "리랭킹 후 순위": after_rank,
            "순위 변화": f"+{change}" if change > 0 else str(change)
        })

    return changes


def print_comparison_tables(comparison):
    """리랭킹 전후 비교 테이블을 출력합니다."""
    query = comparison["query"]
    console.print(f"\n[bold]쿼리:[/bold] {query}")

    # 이전 결과 테이블
    before_table = Table(title="리랭킹 전 (Vector Search 순위)")
    before_table.add_column("순위", style="cyan", justify="center")
    before_table.add_column("문서 ID", style="yellow")
    before_table.add_column("Vector 점수", style="green")
    before_table.add_column("내용 미리보기", style="white")

    for item in comparison["before"][:5]:
        before_table.add_row(
            str(item["rank"]),
            item["id"],
            f"{item['score']:.3f}",
            item["content_preview"]
        )

    # 이후 결과 테이블
    after_table = Table(title="리랭킹 후 (Cross-Encoder 순위)")
    after_table.add_column("순위", style="cyan", justify="center")
    after_table.add_column("문서 ID", style="yellow")
    after_table.add_column("CE 점수", style="green")
    after_table.add_column("내용 미리보기", style="white")

    for item in comparison["after"]:
        after_table.add_row(
            str(item["rank"]),
            item["id"],
            f"{item['score']:.3f}",
            item["content_preview"]
        )

    console.print(before_table)
    console.print(after_table)


def run_reranker_experiment():
    """리랭커 실험 전체를 실행합니다."""
    console.rule("[bold blue]ex08 ReRanker 실험[/bold blue]")

    reranker = create_reranker(use_simple=False)

    test_queries = [
        "연차 신청 절차는 어떻게 됩니까",
        "재택근무 신청 조건",
        "출장비 정산 기한"
    ]

    all_changes = []

    for query in test_queries:
        console.print(f"\n[bold cyan]쿼리:[/bold cyan] {query}")

        initial_results = simulate_initial_retrieval(
            query, SAMPLE_DOCUMENTS, top_k=10
        )
        console.print(f"  초기 검색 결과: {len(initial_results)}개")

        start_time = time.time()
        reranked_results = reranker.rerank(query, initial_results, top_k=5)
        elapsed = time.time() - start_time
        console.print(f"  리랭킹 완료: {len(reranked_results)}개 ({elapsed:.3f}s)")

        # 비교 테이블 출력
        comparison = compare_before_after_reranking(
            query, initial_results[:5], reranked_results
        )
        print_comparison_tables(comparison)

        # 순위 변화 계산
        changes = calculate_rank_change(
            comparison["before"], comparison["after"]
        )
        all_changes.extend(changes)

    console.rule("[bold green]실험 완료[/bold green]")
    console.print(
        "\n[bold]리랭킹 효과 요약:[/bold]\n"
        "  - top_k=10으로 넓게 검색 후 Cross-Encoder로 top_k=5 정제\n"
        "  - 단순 벡터 유사도보다 질문-문서 관련성 정확도 향상\n"
        "  - 처리 시간 증가 (문서당 Cross-Encoder 추론 필요)\n"
        "  - 권장: ReRanker는 top_k가 클 때 (>10) 효과가 극대화됨"
    )


if __name__ == "__main__":
    run_reranker_experiment()
