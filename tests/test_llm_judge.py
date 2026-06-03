from utils.openai_client import generate_ai_response
from evaluations.llm_judge import evaluate_with_llm_judge


def test_llm_judge():

    prompt = "Explain CI/CD in simple terms."

    answer = generate_ai_response(prompt)

    evaluation = evaluate_with_llm_judge(answer)

    print("\nANSWER:\n")
    print(answer)

    print("\nLLM JUDGE:\n")
    print(evaluation)

    assert "score" in evaluation