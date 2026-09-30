from collections.abc import Sequence
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.dependencies import (
    get_provider_comparison_service,
)
from services.provider_comparison_service import (
    ProviderComparisonResult,
    ProviderConfiguration,
)


class StubProviderComparisonService:

    def __init__(
        self,
        result: ProviderComparisonResult
    ):
        self._result = result
        self.received_prompt: str | None = None
        self.received_providers: list[
            ProviderConfiguration
        ] = []

    def compare(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration]
    ) -> list[ProviderComparisonResult]:
        self.received_prompt = prompt
        self.received_providers = list(providers)

        return [self._result]
class NeverCalledComparisonService:

    def compare(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration]
    ) -> list[ProviderComparisonResult]:
        raise AssertionError(
            "The service must not receive invalid requests."
        )
class RejectingComparisonService:

    def compare(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration]
    ) -> list[ProviderComparisonResult]:
        raise ValueError(
            "Comparison request is invalid."
        )
def test_comparison_returns_service_results(
    api_app: FastAPI,
    api_client: TestClient
) -> None:
    expected_result = ProviderComparisonResult(
        provider_name="mock",
        model="mock-model",
        response="API response",
        latency_ms=12.5,
        success=True,
        error=None,
        input_tokens=10,
        output_tokens=5,
        total_tokens=15,
        cached_input_tokens=2,
        reasoning_tokens=1,
        estimated_uncached_input_cost_usd=0.000004,
        estimated_cached_input_cost_usd=0.0000002,
        estimated_output_cost_usd=0.000008,
        estimated_total_cost_usd=0.0000122,
        pricing_tier="standard_paid",
        pricing_effective_date="2026-08-20",
        cost_error=None
    )

    comparison_service = (
        StubProviderComparisonService(expected_result)
    )

    api_app.dependency_overrides[
        get_provider_comparison_service
    ] = lambda: comparison_service

    response = api_client.post(
        "/api/v1/provider-comparisons",
        json={
            "prompt": "  Explain regression testing.  ",
            "providers": [
                {
                    "provider_name": "  mock  ",
                    "model": "  mock-model  ",
                    "provider_options": {
                        "response_prefix": "API"
                    }
                }
            ]
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "prompt": "Explain regression testing.",
        "results": [expected_result.to_dict()]
    }

    assert comparison_service.received_prompt == (
        "Explain regression testing."
    )
    assert comparison_service.received_providers == [
        ProviderConfiguration(
            provider_name="mock",
            model="mock-model",
            provider_options={
                "response_prefix": "API"
            }
        )
    ]
def test_comparison_rejects_blank_prompt(
    api_app: FastAPI,
    api_client: TestClient
) -> None:
    comparison_service = (
        NeverCalledComparisonService()
    )

    api_app.dependency_overrides[
        get_provider_comparison_service
    ] = lambda: comparison_service

    response = api_client.post(
        "/api/v1/provider-comparisons",
        json={
            "prompt": " ",
            "providers": [
                {
                    "provider_name": "mock",
                    "model": "mock-model"
                }
            ]
        }
    )

    assert response.status_code == 422

    error_locations = [
        error["loc"]
        for error in response.json()["detail"]
    ]

    assert ["body", "prompt"] in error_locations
@pytest.mark.parametrize(
    (
        "payload",
        "expected_error_location"
    ),
    [
        (
            {
                "prompt": "Explain regression testing.",
                "providers": []
            },
            ["body", "providers"]
        ),
        (
            {
                "prompt": "Explain regression testing.",
                "providers": [
                    {
                        "provider_name": " ",
                        "model": "mock-model"
                    }
                ]
            },
            [
                "body",
                "providers",
                0,
                "provider_name"
            ]
        ),
        (
            {
                "prompt": "Explain regression testing.",
                "providers": [
                    {
                        "provider_name": "mock",
                        "model": " "
                    }
                ]
            },
            [
                "body",
                "providers",
                0,
                "model"
            ]
        ),
        (
            {
                "prompt": "Explain regression testing.",
                "providers": [
                    {
                        "provider_name": "mock",
                        "model": "mock-model"
                    }
                ],
                "unexpected_field": True
            },
            ["body", "unexpected_field"]
        )
    ],
    ids=[
        "empty-providers",
        "blank-provider-name",
        "blank-model",
        "unexpected-field"
    ]
)
def test_comparison_rejects_other_invalid_requests(
    api_app: FastAPI,
    api_client: TestClient,
    payload: dict[str, object],
    expected_error_location: list[str | int]
) -> None:
    comparison_service = (
        NeverCalledComparisonService()
    )

    api_app.dependency_overrides[
        get_provider_comparison_service
    ] = lambda: comparison_service

    response = api_client.post(
        "/api/v1/provider-comparisons",
        json=payload
    )

    assert response.status_code == 422

    error_locations = [
        error["loc"]
        for error in response.json()["detail"]
    ]

    assert expected_error_location in error_locations
def test_comparison_translates_service_value_error(
    api_app: FastAPI,
    api_client: TestClient
) -> None:
    comparison_service = (
        RejectingComparisonService()
    )

    api_app.dependency_overrides[
        get_provider_comparison_service
    ] = lambda: comparison_service

    response = api_client.post(
        "/api/v1/provider-comparisons",
        json={
            "prompt": "Explain regression testing.",
            "providers": [
                {
                    "provider_name": "mock",
                    "model": "mock-model"
                }
            ]
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Comparison request is invalid."
    }
def test_comparison_preserves_provider_failure(
    api_app: FastAPI,
    api_client: TestClient
) -> None:
    failed_result = ProviderComparisonResult(
        provider_name="gemini",
        model="gemini-test-model",
        response=None,
        latency_ms=25.0,
        success=False,
        error="RuntimeError: Provider unavailable"
    )

    comparison_service = (
        StubProviderComparisonService(failed_result)
    )

    api_app.dependency_overrides[
        get_provider_comparison_service
    ] = lambda: comparison_service

    response = api_client.post(
        "/api/v1/provider-comparisons",
        json={
            "prompt": "Explain regression testing.",
            "providers": [
                {
                    "provider_name": "gemini",
                    "model": "gemini-test-model"
                }
            ]
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "prompt": "Explain regression testing.",
        "results": [failed_result.to_dict()]
    }
def test_openapi_documents_provider_comparison(
    api_client: TestClient
) -> None:
    response = api_client.get("/openapi.json")

    assert response.status_code == 200

    operation = response.json()["paths"][
        "/api/v1/provider-comparisons"
    ]["post"]

    assert operation["summary"] == (
        "Compare LLM providers"
    )

    request_schema = operation["requestBody"][
        "content"
    ]["application/json"]["schema"]

    assert request_schema["$ref"] == (
        "#/components/schemas/"
        "ProviderComparisonRequest"
    )

    response_schema = operation["responses"]["200"][
        "content"
    ]["application/json"]["schema"]

    assert response_schema["$ref"] == (
        "#/components/schemas/"
        "ProviderComparisonResponse"
    )

    assert "400" in operation["responses"]
    assert "422" in operation["responses"]
def test_comparison_executes_real_mock_provider(
    api_client: TestClient
) -> None:
    response = api_client.post(
        "/api/v1/provider-comparisons",
        json={
            "prompt": "Explain regression testing.",
            "providers": [
                {
                    "provider_name": "mock",
                    "model": "mock-model"
                }
            ]
        }
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["prompt"] == (
        "Explain regression testing."
    )
    assert len(payload["results"]) == 1

    result = payload["results"][0]

    assert result["provider_name"] == "mock"
    assert result["model"] == "mock-model"
    assert result["response"] == (
        "mock AI response generated by mock-model: "
        "Explain regression testing."
    )
    assert result["success"] is True
    assert result["error"] is None
    assert result["latency_ms"] >= 0
    assert result["total_tokens"] == 0
    assert result["estimated_total_cost_usd"] is None
    assert "Pricing is not configured" in (
        result["cost_error"]
    )