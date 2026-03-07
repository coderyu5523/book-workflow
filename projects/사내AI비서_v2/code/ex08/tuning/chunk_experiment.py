"""ex08 — 청킹 전략 실험 모듈."""

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
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"

# 실험에 사용할 샘플 문서 (ChromaDB 없이도 실행 가능)
SAMPLE_DOCUMENT = """
제1조 (연차유급휴가)
사용자는 1년간 80퍼센트 이상 출근한 근로자에게 15일의 유급휴가를 주어야 한다.
사용자는 3년 이상 계속하여 근로한 근로자에게는 제1항에 따른 휴가에 최초 1년을 초과하는
계속 근로 연수 매 2년에 대하여 1일을 가산한 유급휴가를 주어야 한다.
이 경우 가산휴가를 포함한 총 휴가 일수는 25일을 한도로 한다.

제2조 (휴가 신청 절차)
근로자가 연차유급휴가를 사용하고자 할 때에는 사용 예정일 3일 전까지
인사담당자에게 서면으로 신청하여야 한다.
단, 긴급한 경우에는 구두로 신청할 수 있으며, 사후에 서면으로 제출하여야 한다.
팀장은 업무 상황을 고려하여 휴가 시기를 조정할 수 있으나, 이 경우에도 근로자의
휴가 사용 권리를 침해하여서는 아니 된다.

제3조 (재택근무 정책)
재택근무는 입사 후 6개월이 경과한 정규직 직원에 한하여 신청할 수 있다.
재택근무 신청은 팀장의 사전 승인을 받아야 하며, 최대 주 2회까지 허용된다.
재택근무 중에도 정규 근무시간(09:00~18:00)을 준수하여야 하며,
화상회의 등 팀 협업에 성실히 참여하여야 한다.

제4조 (출장 규정)
업무상 출장이 필요한 경우, 출발 전일까지 팀장 승인을 받아야 한다.
출장비는 출장 완료 후 5영업일 이내에 영수증과 함께 정산 신청하여야 한다.
숙박비는 1박당 15만원을 초과할 수 없으며, 식비는 1일 5만원을 한도로 한다.
해외 출장의 경우 별도의 해외 출장 규정을 따른다.

제5조 (성과 평가)
성과 평가는 상반기(7월)와 하반기(1월)에 각 1회 실시한다.
평가 항목은 목표달성도(60%), 역량평가(30%), 동료평가(10%)로 구성된다.
평가 등급은 S(상위 10%), A(상위 30%), B(중위 40%), C(하위 15%), D(하위 5%)로 한다.
평가 결과는 개인별로 통보되며, 이의가 있는 경우 결과 통보 후 5영업일 이내에
인사팀에 이의 신청할 수 있다.

제6조 (복리후생)
회사는 직원의 자기계발을 위해 연간 50만원 한도에서 자기계발비를 지원한다.
지원 가능한 항목은 직무 관련 도서, 온라인 강의, 자격증 취득 비용이다.
신청은 분기별로 받으며, 영수증 제출이 필요하다.
건강검진은 연 1회 전액 회사 부담으로 실시한다.
"""


def load_sample_document():
    """실험용 샘플 문서를 반환합니다."""
    return SAMPLE_DOCUMENT.strip()


def load_document_from_file(file_path):
    """파일에서 문서를 로드합니다."""
    if not file_path.exists():
        print(f"문서 파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def fixed_size_chunking(text, chunk_size=500, overlap=50):
    """고정 크기 청킹을 수행합니다."""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        if end >= text_length:
            break

        start = end - overlap

    return chunks


def recursive_character_chunking(text, chunk_size=500, chunk_overlap=50):
    """재귀적 문자 분할 청킹을 수행합니다."""
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", ".", " ", ""]
        )
        chunks = splitter.split_text(text)
        return chunks

    except ImportError:
        console.print(
            "[yellow]langchain_text_splitters 가 설치되지 않아 "
            "기본 청킹으로 대체합니다.[/yellow]"
        )
        return fixed_size_chunking(text, chunk_size, chunk_overlap)


def semantic_chunking(text, embedding_model="jhgan/ko-sroberta-multitask", breakpoint_threshold_type="percentile"):
    """의미 단위 기반 시맨틱 청킹을 수행합니다."""
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_experimental.text_splitter import SemanticChunker

        console.print("[dim]시맨틱 청킹: 임베딩 모델 로드 중...[/dim]")
        embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cpu"}
        )

        chunker = SemanticChunker(
            embeddings,
            breakpoint_threshold_type=breakpoint_threshold_type
        )
        chunks = chunker.split_text(text)
        return chunks

    except ImportError:
        console.print(
            "[yellow]langchain_experimental 패키지가 없어 "
            "재귀 청킹으로 대체합니다.[/yellow]"
        )
        console.print("pip install langchain-experimental 을 실행하십시오.")
        return recursive_character_chunking(text, chunk_size=500, chunk_overlap=50)


def analyze_chunks(chunks):
    """청크 분석 통계를 계산합니다."""
    if not chunks:
        return {"count": 0, "avg_size": 0, "min_size": 0, "max_size": 0}

    sizes = [len(c) for c in chunks]
    return {
        "count": len(chunks),
        "avg_size": sum(sizes) / len(sizes),
        "min_size": min(sizes),
        "max_size": max(sizes)
    }


def run_chunk_size_experiment(text):
    """청크 크기 실험 (300/500/1000자)을 실행합니다."""
    results = []
    chunk_sizes = [300, 500, 1000]

    for size in chunk_sizes:
        overlap = size // 10  # 10% 오버랩
        start_time = time.time()
        chunks = fixed_size_chunking(text, chunk_size=size, overlap=overlap)
        elapsed = time.time() - start_time

        stats = analyze_chunks(chunks)
        results.append({
            "전략": f"Fixed-size ({size}자)",
            "청크 수": stats["count"],
            "평균 크기": f"{stats['avg_size']:.0f}자",
            "최소 크기": f"{stats['min_size']}자",
            "최대 크기": f"{stats['max_size']}자",
            "실행 시간": f"{elapsed:.3f}s"
        })

    return results


def run_overlap_experiment(text):
    """오버랩 비율 실험 (10%/20%/30%)을 실행합니다."""
    results = []
    chunk_size = 500
    overlap_ratios = [0.1, 0.2, 0.3]

    for ratio in overlap_ratios:
        overlap = int(chunk_size * ratio)
        chunks = fixed_size_chunking(text, chunk_size=chunk_size, overlap=overlap)
        stats = analyze_chunks(chunks)

        results.append({
            "오버랩 비율": f"{int(ratio*100)}%",
            "오버랩 문자 수": f"{overlap}자",
            "청크 수": stats["count"],
            "평균 크기": f"{stats['avg_size']:.0f}자"
        })

    return results


def run_strategy_comparison(text):
    """청킹 전략 비교 실험 (Fixed vs Recursive vs Semantic)을 실행합니다."""
    results = []

    # 1. Fixed-size 청킹
    start = time.time()
    fixed_chunks = fixed_size_chunking(text, chunk_size=500, overlap=50)
    fixed_stats = analyze_chunks(fixed_chunks)
    results.append({
        "전략": "Fixed-size (500자)",
        "청크 수": fixed_stats["count"],
        "평균 크기": f"{fixed_stats['avg_size']:.0f}자",
        "실행 시간": f"{time.time()-start:.3f}s",
        "특징": "균일한 크기, 빠른 처리"
    })

    # 2. Recursive 청킹
    start = time.time()
    recursive_chunks = recursive_character_chunking(text, chunk_size=500, chunk_overlap=50)
    recursive_stats = analyze_chunks(recursive_chunks)
    results.append({
        "전략": "Recursive Character",
        "청크 수": recursive_stats["count"],
        "평균 크기": f"{recursive_stats['avg_size']:.0f}자",
        "실행 시간": f"{time.time()-start:.3f}s",
        "특징": "문단/문장 경계 존중"
    })

    # 3. Semantic 청킹 (모델 로드 시간이 있을 수 있음)
    console.print("[dim]시맨틱 청킹 실험 중...[/dim]")
    start = time.time()
    semantic_chunks = semantic_chunking(text)
    semantic_stats = analyze_chunks(semantic_chunks)
    results.append({
        "전략": "Semantic Chunking",
        "청크 수": semantic_stats["count"],
        "평균 크기": f"{semantic_stats['avg_size']:.0f}자",
        "실행 시간": f"{time.time()-start:.3f}s",
        "특징": "의미 단위 분할, 최고 품질"
    })

    return results


def print_experiment_table(title, results):
    """실험 결과를 Rich 테이블로 출력합니다."""
    if not results:
        console.print("[red]결과가 없습니다.[/red]")
        return

    table = Table(title=title)
    for col in results[0].keys():
        table.add_column(col, style="cyan")

    for row in results:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)


def run_all_experiments():
    """모든 청킹 실험을 순서대로 실행합니다."""
    console.rule("[bold blue]ex08 청킹 전략 실험[/bold blue]")

    text = load_sample_document()
    console.print(f"[green]샘플 문서 로드:[/green] {len(text)}자")

    console.print("\n[bold yellow]1. 청크 크기 실험 (300/500/1000자)[/bold yellow]")
    size_results = run_chunk_size_experiment(text)
    print_experiment_table("청크 크기별 비교", size_results)

    console.print("\n[bold yellow]2. 오버랩 비율 실험 (10%/20%/30%)[/bold yellow]")
    overlap_results = run_overlap_experiment(text)
    print_experiment_table("오버랩 비율별 비교", overlap_results)

    console.print("\n[bold yellow]3. 청킹 전략 비교 (Fixed vs Recursive vs Semantic)[/bold yellow]")
    strategy_results = run_strategy_comparison(text)
    print_experiment_table("청킹 전략 비교", strategy_results)

    console.rule("[bold green]실험 완료[/bold green]")
    console.print(
        "\n[bold]권장 설정:[/bold]\n"
        "  - 빠른 처리 필요: Fixed-size (500자, 20% 오버랩)\n"
        "  - 균형 잡힌 성능: Recursive Character (500자, 50자 오버랩)\n"
        "  - 최고 품질 목표: Semantic Chunking (임베딩 모델 필요)"
    )


if __name__ == "__main__":
    run_all_experiments()
