from fastapi import FastAPI

from api.routers.health import router as health_router
from api.routers.provider_comparison import (
    router as provider_comparison_router,
)


def create_app() -> FastAPI:
    application = FastAPI(
        title="AI Quality Evaluation Platform API",
        description=(
            "REST API for AI quality evaluation, "
            "provider comparison, and benchmarking."
        ),
        version="0.1.0"
    )

    application.include_router(health_router)
    application.include_router(
        provider_comparison_router
    )

    return application


app = create_app()