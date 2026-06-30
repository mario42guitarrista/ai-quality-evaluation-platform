from utils.prompt_loader import load_prompts_from_folder
from services.llm_service import generate_response_with_provider
from evaluations.response_evaluator import evaluate_response
from evaluations.llm_judge import evaluate_with_llm_judge
from utils.evaluation_reporter import save_evaluation_report


def run_multi_prompt_evaluation():
    prompts = load_prompts_from_folder()

    results = []

    for item in prompts:
        prompt_name = item["name"]
        prompt = item["prompt"]
        expected_keywords = item["expected_keywords"]

        print(f"\nRunning evaluation for: {prompt_name}")

        response = generate_response_with_provider(
        prompt=prompt,
        provider_name="openai",
        model="gpt-4.1-mini"
        )

        evaluation = evaluate_response(
            response=response,
            expected_keywords=expected_keywords
        )

        llm_judge = evaluate_with_llm_judge(response)

        report_path = save_evaluation_report(
            prompt=prompt,
            response=response,
            evaluation=evaluation,
            llm_judge=llm_judge
        )

        results.append({
            "prompt_name": prompt_name,
            "prompt": prompt,
            "expected_keywords": expected_keywords,
            "evaluation": evaluation,
            "llm_judge": llm_judge,
            "report_path": report_path
        })

    return results


if __name__ == "__main__":
    results = run_multi_prompt_evaluation()

    print("\nLLM JUDGE EVALUATION RESULTS:\n")

    for result in results:
        print(result)