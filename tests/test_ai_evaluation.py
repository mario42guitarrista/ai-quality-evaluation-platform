from utils.openai_client import generate_ai_response
from evaluations.response_evaluator import evaluate_response
from utils.evaluation_reporter import save_evaluation_report


def test_ai_response_evaluation():

    prompt = "Explain CI/CD in simple terms."

    expected_keywords = [
        "automation",
        "testing",
        "deployment",
        "integration"
    ]

    response = generate_ai_response(prompt)

    evaluation = evaluate_response(
        response=response,
        expected_keywords=expected_keywords
    )

    report_path = save_evaluation_report(
        prompt=prompt,
        response=response,
        evaluation=evaluation
    )

    print("\nAI RESPONSE:\n")
    print(response)

    print("\nEVALUATION:\n")
    print(evaluation)

    print("\nREPORT SAVED AT:\n")
    print(report_path)

    assert evaluation["approved"] is True