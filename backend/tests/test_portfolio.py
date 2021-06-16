from ast import literal_eval
from typing import Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_401_UNAUTHORIZED

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
    async def test_valid_input_creates_portfolio(self, app: FastAPI, authorized_client: AsyncClient,
                                                 test_post_body: Dict) -> None:
        res = await authorized_client.post(app.url_path_for("portfolio:post"), json=test_post_body)
        assert res.status_code != HTTP_404_NOT_FOUND
        assert res.status_code == HTTP_201_CREATED
        assert list(res.json().keys()) == ['id', 'user_id', 'portfolio_weights', 'returns', 'std', 'sharpe_ratio',
                                           'return_over_risk', 'added_at', 'updated_at']
        assert test_post_body['securities'] == list(literal_eval(res.json()['portfolio_weights']).keys())

    async def test_invalid_input_raises_error(self, app: FastAPI, authorized_client: AsyncClient,
                                              test_invalid_post_body: Dict) -> None:
        res = await authorized_client.post(app.url_path_for("portfolio:post"), data=test_invalid_post_body)
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    async def test_unauthenticated_posts_no_portfolio(self, app: FastAPI, client: AsyncClient,
                                                      test_post_body: Dict) -> None:
        res = await client.post(app.url_path_for("portfolio:post"), json=test_post_body)
        assert res.status_code == HTTP_401_UNAUTHORIZED


class TestGetAllPortfolios:
    async def test_valid_input_get_all_portfolios(self, app: FastAPI, authorized_client: AsyncClient) -> None:
        res = await authorized_client.get(app.url_path_for("portfolio:get-all"))
        assert res.status_code == HTTP_200_OK
        assert list(res.json()[0].keys()) == ['id', 'user_id', 'portfolio_weights', 'returns', 'std', 'sharpe_ratio',
                                              'return_over_risk', 'added_at', 'updated_at']

    async def test_new_user_gets_no_portfolios(self, app: FastAPI, authorized_client_new: AsyncClient) -> None:
        # new user who has yet to post any portfolios returns an empty list
        res = await authorized_client_new.get(app.url_path_for("portfolio:get-all"))
        assert res.status_code == HTTP_200_OK
        assert res.json() == []

    async def test_unauthenticated_gets_no_portfolio(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("portfolio:get-all"))
        assert res.status_code == HTTP_401_UNAUTHORIZED


class TestGetPortfolioByID:
    async def test_valid_input_gets_portfolio(self, app: FastAPI, authorized_client: AsyncClient) -> None:
        res = await authorized_client.get(app.url_path_for("portfolio:get-by-id", portfolio_id="1"))
        assert res.status_code == HTTP_200_OK
        assert list(res.json().keys()) == ['id', 'user_id', 'portfolio_weights', 'returns', 'std', 'sharpe_ratio',
                                           'return_over_risk', 'added_at', 'updated_at']

    @pytest.mark.parametrize("invalid_id, status_code",
                             ((999, 404),
                              (-1, 404),
                              ("INVALID", 422),
                              ([1, 2], 422),), )
    async def test_invalid_input_gets_error(self, app: FastAPI, authorized_client: AsyncClient, invalid_id, status_code
                                            ) -> None:
        res = await authorized_client.get(app.url_path_for("portfolio:get-by-id", portfolio_id=invalid_id))
        assert res.status_code == status_code

    async def test_unauthenticated_gets_no_portfolio(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("portfolio:get-by-id", portfolio_id="1"))
        assert res.status_code == HTTP_401_UNAUTHORIZED


class TestDeleteAllPortfolios:
    async def test_valid_input_deletes_all_portfolios(self, app: FastAPI, authorized_client: AsyncClient) -> None:
        res = await authorized_client.get(app.url_path_for("portfolio:get-all"))
        assert res.status_code == HTTP_200_OK
        assert list(res.json()[0].keys()) == ['id', 'user_id', 'portfolio_weights', 'returns', 'std', 'sharpe_ratio',
                                              'return_over_risk', 'added_at', 'updated_at']

    async def test_new_user_deletes_no_portfolios(self, app: FastAPI, authorized_client_new: AsyncClient) -> None:
        # new user who has yet to post any portfolios returns an empty list
        res = await authorized_client_new.get(app.url_path_for("portfolio:get-all"))
        assert res.status_code == HTTP_200_OK
        assert res.json() == []

    async def test_unauthenticated_deletes_no_portfolios(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get(app.url_path_for("portfolio:get-all"))
        assert res.status_code == HTTP_401_UNAUTHORIZED


class TestDeletePortfolioByID:
    async def test_valid_input_deletes_portfolio(self, app: FastAPI, authorized_client: AsyncClient) -> None:
        res = await authorized_client.delete(app.url_path_for("portfolio:delete-by-id", portfolio_id="1"))
        assert res.status_code == HTTP_200_OK
        assert list(res.json().keys()) == ['id', 'user_id', 'portfolio_weights', 'returns', 'std', 'sharpe_ratio',
                                           'return_over_risk', 'added_at', 'updated_at']

    @pytest.mark.parametrize("invalid_id, status_code",
                             ((999, 404),
                              (-1, 404),
                              ("INVALID", 422),
                              ([1, 2], 422),), )
    async def test_invalid_input_gets_error(self, app: FastAPI, authorized_client: AsyncClient, invalid_id, status_code
                                            ) -> None:
        res = await authorized_client.get(app.url_path_for("portfolio:delete-by-id", portfolio_id=invalid_id))
        assert res.status_code == status_code
