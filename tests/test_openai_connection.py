from utils.openai_client import generate_ai_response


def test_openai_connection():

    prompt = "Explain CI/CD in simple terms."

    response = generate_ai_response(prompt)

    print("\nAI RESPONSE:\n")
    print(response)

    assert response is not None
    assert len(response) > 0