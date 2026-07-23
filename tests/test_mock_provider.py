from providers.mock_provider import MockProvider
from services.llm_service import generate_response_with_provider


def test_mock_provider_generates_response():
    provider = MockProvider(model="mock-model")

    response = provider.generate_response(
        prompt="Explain CI/CD in simple terms."
    )

    assert response is not None
    assert "mock AI response" in response
    assert "mock-model" in response
    assert "Explain CI/CD" in response


def test_llm_service_uses_mock_provider():
    response = generate_response_with_provider(
        prompt="Explain Python functions in simple terms.",
        provider_name="mock",
        model="mock-model"
    )

    assert response is not None
    assert "mock AI response" in response
    assert "mock-model" in response
    assert "Explain Python functions" in response