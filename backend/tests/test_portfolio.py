import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from app.models.portfolio import PortfolioPOSTBodyParams, StrictDate
from typing import List, Dict

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture()
def test_post_body():
    return {"securities": ["AAPL", "AMZN"],
            "start": "2000-01-01",
            "end": "2020-01-01"}


@pytest.fixture()
def test_invalid_post_body():
    return {"INVALID": ["AAPL", "AMZN"],
            "start": "2000-01-01",
            "end": "2020-01-01"}

class TestPOSTPortfolio:
    async def test_routes_exist(self, app: FastAPI, authorized_client: AsyncClient,
                                test_post_body: Dict) -> None:

        res = await authorized_client.post(app.url_path_for("portfolio:post"), json=test_post_body)
        assert res.status_code == HTTP_200_OK

    async def test_invalid_input_raises_error(self, app: FastAPI, authorized_client: AsyncClient,
                                              test_invalid_post_body: Dict) -> None:
        res = await authorized_client.post(app.url_path_for("portfolio:post"), data=test_invalid_post_body)
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
