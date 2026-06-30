import json
import os
from datetime import datetime

from services.llm_service import generate_response_with_provider
from evaluations.llm_judge import evaluate_with_llm_judge


MODELS = [
    "gpt-4.1-mini",
    "gpt-4.1"
]


PROMPT = """
Explain CI/CD in simple terms.
"""


def save_model_benchmark_report(prompt, results):
    os.makedirs("reports/model_benchmarks", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "timestamp": timestamp,
        "benchmark_type": "multi_model",
        "prompt": prompt.strip(),
        "results": results
    }

    file_path = f"reports/model_benchmarks/model_benchmark_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    return file_path


def run_model_benchmark():

    results = []

    for model in MODELS:

        print(f"\nTesting model: {model}")

        response = generate_response_with_provider(
        prompt=PROMPT,
        provider_name="openai",
        model=model
        )

        judge = evaluate_with_llm_judge(
            response
        )

        results.append({
            "model": model,
            "judge_score": judge["score"],
            "accuracy": judge["accuracy"],
            "clarity": judge["clarity"],
            "completeness": judge["completeness"],
            "comments": judge["comments"]
        })

    results.sort(
        key=lambda x: x["judge_score"],
        reverse=True
    )

    report_path = save_model_benchmark_report(
        prompt=PROMPT,
        results=results
    )

    return results, report_path


if __name__ == "__main__":

    benchmark, report_path = run_model_benchmark()

    print("\nMODEL BENCHMARK\n")

    for position, item in enumerate(
        benchmark,
        start=1
    ):

        print(
            f"{position}. "
            f"{item['model']} "
            f"(Judge Score: {item['judge_score']})"
        )

    print("\nREPORT SAVED AT:")
    print(report_path)