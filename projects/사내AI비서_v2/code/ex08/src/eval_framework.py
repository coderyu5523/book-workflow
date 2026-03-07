"""ex08 — RAG 품질 평가 프레임워크 모듈."""

import json
import os
import sys
import time
from datetime import datetime
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
TEST_QUESTIONS_PATH = DATA_DIR / "test_questions.json"

USE_RAGAS = os.getenv("USE_RAGAS", "false").lower() == "true"


def load_test_questions(path=TEST_QUESTIONS_PATH):
    """테스트 질문 파일을 로드한다."""
    if not path.exists():
        print(f"테스트 질문 파일을 찾을 수 없습니다: {path}")
        print("data/test_questions.json 파일이 있는지 확인하십시오.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    console.print(f"[green]테스트 질문 로드 완료:[/green] {len(questions)}개")
    return questions


def filter_questions_by_category(questions, category=None):
    """카테고리별로 질문을 필터링한다."""
    if category is None:
        return questions
    return [q for q in questions if q.get("category") == category]


def calculate_precision_at_k(retrieved_sources, relevant_sources, k):
    """Precision@k를 계산한다."""
    if k == 0 or not retrieved_sources:
        return 0.0

    top_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)

    hits = sum(1 for src in top_k if any(rel in src for rel in relevant_set))
    return hits / k


def calculate_recall_at_k(retrieved_sources, relevant_sources, k):
    """Recall@k를 계산한다."""
    if not relevant_sources:
        return 0.0

    top_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)

    hits = sum(
        1 for rel in relevant_set
        if any(rel in src for src in top_k)
    )
    return hits / len(relevant_set)


def calculate_mrr(retrieved_sources, relevant_sources):
    """Mean Reciprocal Rank(MRR)를 계산한다."""
    relevant_set = set(relevant_sources)

    for rank, src in enumerate(retrieved_sources, start=1):
        if any(rel in src for rel in relevant_set):
            return 1.0 / rank

    return 0.0


def estimate_hallucination_rate(answers, contexts):
    """환각(Hallucination) 발생률을 추정한다."""
    hallucination_count = 0

    for answer, context_docs in zip(answers, contexts):
        if not context_docs:
            hallucination_count += 1
            continue

        context_combined = " ".join(context_docs).lower()
        answer_words = set(answer.lower().split())
        context_words = set(context_combined.split())

        # 답변 핵심 단어가 컨텍스트에 없으면 환각으로 간주
        key_words = [w for w in answer_words if len(w) > 3]
        if key_words:
            overlap_ratio = len(
                [w for w in key_words if w in context_words]
            ) / len(key_words)
            if overlap_ratio < 0.3:
                hallucination_count += 1

    return hallucination_count / len(answers) if answers else 0.0


def run_ragas_evaluation(questions, answers, contexts, ground_truths):
    """RAGAS 프레임워크로 평가를 실행한다."""
    if not USE_RAGAS:
        console.print(
            "[yellow]RAGAS 평가가 비활성화되어 있습니다. "
            "USE_RAGAS=true 를 설정하고 ragas 패키지를 설치하십시오.[/yellow]"
        )
        return {"faithfulness": None, "answer_relevancy": None}

    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import answer_relevancy, faithfulness

        data = {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths
        }
        dataset = Dataset.from_dict(data)
        result = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

        return {
            "faithfulness": float(result["faithfulness"]),
            "answer_relevancy": float(result["answer_relevancy"])
        }

    except ImportError:
        console.print(
            "[red]ragas 또는 datasets 패키지가 설치되지 않았습니다.[/red]"
        )
        console.print("pip install ragas datasets 를 실행하십시오.")
        return {"faithfulness": None, "answer_relevancy": None}


def run_retrieval_evaluation(experiment_name, retrieved_results, questions, k_values=None):
    """검색 성능을 평가한다."""
    if k_values is None:
        k_values = [3, 5, 10]

    metrics = {f"precision@{k}": [] for k in k_values}
    metrics.update({f"recall@{k}": [] for k in k_values})
    metrics["mrr"] = []

    for question, result in zip(questions, retrieved_results):
        expected_source = question.get("expected_source", "")
        relevant_sources = [expected_source] if expected_source else []
        retrieved_sources = result.get("sources", [])

        for k in k_values:
            p_at_k = calculate_precision_at_k(retrieved_sources, relevant_sources, k)
            r_at_k = calculate_recall_at_k(retrieved_sources, relevant_sources, k)
            metrics[f"precision@{k}"].append(p_at_k)
            metrics[f"recall@{k}"].append(r_at_k)

        mrr = calculate_mrr(retrieved_sources, relevant_sources)
        metrics["mrr"].append(mrr)

    # 평균 계산
    avg_metrics = {
        key: sum(vals) / len(vals) if vals else 0.0
        for key, vals in metrics.items()
    }

    console.print(f"\n[bold cyan]--- {experiment_name} 평가 결과 ---[/bold cyan]")
    _print_retrieval_metrics_table(avg_metrics, k_values)

    return avg_metrics


def _print_retrieval_metrics_table(metrics, k_values):
    """검색 성능 지표를 테이블로 출력한다."""
    table = Table(title="Retrieval 평가 지표")
    table.add_column("지표", style="cyan")
    table.add_column("값", style="green")

    for k in k_values:
        table.add_row(f"Precision@{k}", f"{metrics[f'precision@{k}']:.4f}")
        table.add_row(f"Recall@{k}", f"{metrics[f'recall@{k}']:.4f}")

    table.add_row("MRR", f"{metrics['mrr']:.4f}")
    console.print(table)


def compare_experiments(before_metrics, after_metrics, before_name="튜닝 전", after_name="튜닝 후"):
    """두 실험의 before/after 성능을 비교한다."""
    comparison = {}

    all_keys = set(before_metrics.keys()) | set(after_metrics.keys())

    for key in all_keys:
        before_val = before_metrics.get(key, 0.0)
        after_val = after_metrics.get(key, 0.0)

        if before_val and before_val > 0:
            improvement = (after_val - before_val) / before_val * 100
            improvement_label = f"+{improvement:.1f}%" if improvement >= 0 else f"{improvement:.1f}%"
        elif before_val == 0.0 and after_val > 0:
            # before가 0이고 after가 개선된 경우
            improvement = None
            improvement_label = "신규 성과"
        else:
            improvement = 0.0
            improvement_label = "변화 없음"

        comparison[key] = {
            before_name: before_val,
            after_name: after_val,
            "개선율(%)": improvement,
            "개선율_표시": improvement_label
        }

    # 비교 테이블 출력
    table = Table(title=f"Before/After 비교: {before_name} vs {after_name}")
    table.add_column("지표", style="cyan")
    table.add_column(before_name, style="yellow")
    table.add_column(after_name, style="green")
    table.add_column("개선율", style="magenta")

    for key, vals in comparison.items():
        label = vals["개선율_표시"]
        improvement_val = vals["개선율(%)"]

        if improvement_val is None:
            # 신규 성과: before=0, after>0
            improvement_str = "[green]신규 성과[/green]"
        elif improvement_val > 0:
            improvement_str = f"[green]+{improvement_val:.1f}%[/green]"
        elif improvement_val < 0:
            improvement_str = f"[red]{improvement_val:.1f}%[/red]"
        else:
            improvement_str = "[dim]변화 없음[/dim]"

        table.add_row(
            key,
            f"{vals[before_name]:.4f}",
            f"{vals[after_name]:.4f}",
            improvement_str
        )

    console.print(table)
    return comparison


def save_evaluation_report(experiment_name, metrics, output_dir=OUTPUTS_DIR):
    """평가 결과를 JSON 파일로 저장한다."""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = experiment_name.replace(" ", "_").replace("/", "_")
    output_path = output_dir / f"eval_{safe_name}_{timestamp}.json"

    report = {
        "experiment_name": experiment_name,
        "timestamp": timestamp,
        "metrics": metrics
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    console.print(f"[green]평가 보고서 저장:[/green] {output_path}")
    return output_path


def create_sample_retrieved_results(questions, simulate_poor=False):
    """테스트용 가상 검색 결과를 생성한다."""
    results = []

    for q in questions:
        expected = q.get("expected_source", "")

        if simulate_poor:
            # 나쁜 검색: 관련 없는 소스들 (정답 소스 미포함)
            sources = [
                "IT_보안정책_v3.0.pdf",
                "재무_출장규정_v2.0.pdf",
                "HR_온보딩가이드_v1.5.pdf",
                "직원DB_무관한항목",
                "알_수_없는_문서.pdf"
            ]
        else:
            # 좋은 검색: 첫 번째에 정답 소스 포함
            sources = [
                expected,
                "HR_취업규칙_v1.0.pdf",
                "HR_복리후생규정_v3.0.pdf",
                "IT_보안정책_v3.0.pdf",
                "재무_출장규정_v2.0.pdf"
            ]

        results.append({
            "question": q["question"],
            "sources": sources,
            "answer": q.get("expected_answer", ""),
            "context": [expected] if expected else []
        })

    return results


def run_full_evaluation_demo():
    """전체 평가 프레임워크 데모를 실행한다."""
    console.rule("[bold blue]ex08 RAG 튜닝 평가 프레임워크 데모[/bold blue]")

    # --- INPUT: 질문 로드 ---
    questions = load_test_questions()

    # 카테고리별 통계 출력
    table = Table(title="테스트 질문 카테고리 분포")
    table.add_column("카테고리", style="cyan")
    table.add_column("개수", style="green")

    for category in ["정형", "비정형", "복합"]:
        filtered = filter_questions_by_category(questions, category)
        table.add_row(category, str(len(filtered)))
    table.add_row("전체", str(len(questions)), style="bold")
    console.print(table)

    # --- PROCESS: 튜닝 전 시뮬레이션 ---
    console.print("\n[bold yellow]1. 튜닝 전 검색 결과 평가[/bold yellow]")
    before_results = create_sample_retrieved_results(questions, simulate_poor=True)
    before_metrics = run_retrieval_evaluation(
        experiment_name="튜닝 전 (기본 Vector Search)",
        retrieved_results=before_results,
        questions=questions,
        k_values=[3, 5, 10]
    )

    # --- PROCESS: 튜닝 후 시뮬레이션 ---
    console.print("\n[bold yellow]2. 튜닝 후 검색 결과 평가[/bold yellow]")
    after_results = create_sample_retrieved_results(questions, simulate_poor=False)
    after_metrics = run_retrieval_evaluation(
        experiment_name="튜닝 후 (Hybrid + ReRanker)",
        retrieved_results=after_results,
        questions=questions,
        k_values=[3, 5, 10]
    )

    # --- PROCESS: Hallucination Rate 추정 ---
    console.print("\n[bold yellow]3. 환각률(Hallucination Rate) 추정[/bold yellow]")
    before_answers = [r["answer"] for r in before_results]
    after_answers = [r["answer"] for r in after_results]
    before_contexts = [r["context"] for r in before_results]
    after_contexts = [r["context"] for r in after_results]

    before_hallucination = estimate_hallucination_rate(before_answers, before_contexts)
    after_hallucination = estimate_hallucination_rate(after_answers, after_contexts)

    console.print(f"  튜닝 전 환각률: [red]{before_hallucination:.1%}[/red]")
    console.print(f"  튜닝 후 환각률: [green]{after_hallucination:.1%}[/green]")

    # RAGAS 평가 (설정 시)
    if USE_RAGAS:
        console.print("\n[bold yellow]4. RAGAS 평가 실행[/bold yellow]")
        ragas_result = run_ragas_evaluation(
            questions=[q["question"] for q in questions],
            answers=after_answers,
            contexts=after_contexts,
            ground_truths=[q["expected_answer"] for q in questions]
        )
        console.print(f"  Faithfulness: {ragas_result.get('faithfulness')}")
        console.print(f"  Answer Relevancy: {ragas_result.get('answer_relevancy')}")

    # --- OUTPUT: Before/After 비교 ---
    console.print("\n[bold yellow]5. Before/After 비교 보고서[/bold yellow]")
    comparison = compare_experiments(
        before_metrics=before_metrics,
        after_metrics=after_metrics,
        before_name="튜닝 전",
        after_name="튜닝 후"
    )

    # 결과 저장
    save_evaluation_report(
        experiment_name="full_comparison",
        metrics={
            "before": before_metrics,
            "after": after_metrics,
            "hallucination": {
                "before": before_hallucination,
                "after": after_hallucination
            }
        }
    )

    console.rule("[bold green]평가 완료[/bold green]")


if __name__ == "__main__":
    run_full_evaluation_demo()
