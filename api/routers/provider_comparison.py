from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.dependencies import (
    ProviderComparisonRunner,
    get_provider_comparison_service,
)
from api.schemas.provider_comparison import (
    ProviderComparisonRequest,
    ProviderComparisonResponse,
    ProviderComparisonResultResponse,
)
from services.provider_comparison_service import (
    ProviderConfiguration,
)


router = APIRouter(
    prefix="/api/v1/provider-comparisons",
    tags=["provider-comparisons"]
)


@router.post(
    "",
    response_model=ProviderComparisonResponse,
    summary="Compare LLM providers",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": (
                "The comparison service rejected "
                "the request."
            )
        }
    }
)
def compare_providers(
    request: ProviderComparisonRequest,
    comparison_service: Annotated[
        ProviderComparisonRunner,
        Depends(get_provider_comparison_service)
    ]
) -> ProviderComparisonResponse:
    configurations = [
        ProviderConfiguration(
            provider_name=provider.provider_name,
            model=provider.model,
            provider_options=dict(
                provider.provider_options
            )
        )
        for provider in request.providers
    ]

    try:
        results = comparison_service.compare(
            prompt=request.prompt,
            providers=configurations
        )
    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception)
        ) from exception

    return ProviderComparisonResponse(
        prompt=request.prompt,
        results=[
            ProviderComparisonResultResponse.model_validate(
                result
            )
            for result in results
        ]
    )