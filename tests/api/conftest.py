from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.main import create_app


@pytest.fixture
def api_app() -> FastAPI:
    return create_app()


@pytest.fixture
def api_client(
    api_app: FastAPI
) -> Iterator[TestClient]:
    with TestClient(api_app) as client:
        yield client