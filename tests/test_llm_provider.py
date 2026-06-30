from services.llm_service import generate_response_with_provider


def test_openai_provider():

    response = generate_response_with_provider(
        prompt="Explain CI/CD in one sentence.",
        provider_name="openai",
        model="gpt-4.1-mini"
    )

    print("\nProvider response:\n")
    print(response)

    assert response is not None
    assert len(response) > 0