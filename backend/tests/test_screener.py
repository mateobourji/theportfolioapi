import random
from typing import List, Dict, Union

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from app.models.equity import EquityInDB
from app.models.etf import ETFInDB

# decorate all tests with @pytest.mark.asyncio
from app.models.fund import FundInDB

pytestmark = pytest.mark.asyncio


def common_assertions(res, assets: Union[List[ETFInDB], List[EquityInDB], List[FundInDB]], filters: Dict):
    assert res.status_code == HTTP_200_OK
    assert isinstance(res.json(), list)
    assert len(res.json()) > 0
    assert assets_meet_filter(assets=assets, filters=filters)


def assets_meet_filter(assets: Union[List[ETFInDB], List[EquityInDB]], filters: Dict):
    for asset in assets:
        for filter in filters.keys():
            if getattr(asset, filter) not in filters[filter]:
                return False
    return True


def get_params(assets, filters, num_filters):
    params = {key: [] for key in filters}
    for asset in random.sample(assets, num_filters):
        for filter in filters:
            params[filter].append(getattr(asset, filter))
    return params


class TestGetEquity:
    @pytest.mark.parametrize(
        "filters, num_filters",
        (
                (["ticker"], 3),
                (["country"], 2),
                (["sector"], 1),
                (["sector", "industry"], 4),
                (["sector", "industry"], 1),
                (["long_name"], 1),
                ([], 1)
        ),
    )
    async def test_valid_filter_gets_equities(
            self, app: FastAPI, authorized_client: AsyncClient, test_equities: List[EquityInDB], filters: List[str],
            num_filters: int) -> None:

        params = get_params(assets=test_equities, filters=filters, num_filters=num_filters)

        res = await authorized_client.get(app.url_path_for("screener:get-equities"), params=params)

        equities_in_db = [EquityInDB(**e) for e in res.json()]
        common_assertions(res=res, assets=equities_in_db, filters=params)


    @pytest.mark.parametrize(
        "filters, parameters, status_code",
        (
                ("ticker", ["INVALID"], 404),
                ("country", -1, 404),
                ("sector", "invalid", 404),
                ("exchange", ["CAC", "FLO"], 404)
        ),
    )
    async def test_invalid_input_raises_error(self, app: FastAPI, authorized_client: AsyncClient, filters: str,
                                              parameters: List[str], status_code: int) -> None:
        params = {filters: parameters}
        res = await authorized_client.get(app.url_path_for("screener:get-equities"), params=params)
        assert res.status_code == status_code


class TestGetETF:
    @pytest.mark.parametrize(
        "filters, num_filters",
        (
                (["family"], 4),
                (["ticker"], 3),
                (["currency"], 2),
                (["category"], 1),
                (["category", "family"], 1),
                (["exchange"], 1),
                (["market"], 2),
                ([], 1)
        ),
    )
    async def test_valid_filter_gets_etfs(
            self, app: FastAPI, authorized_client: AsyncClient, test_etfs: List[ETFInDB], filters: List[str],
            num_filters: int) -> None:

        params = get_params(assets=test_etfs, filters=filters, num_filters=num_filters)

        res = await authorized_client.get(app.url_path_for("screener:get-ETFs"), params=params)

        etfs_in_db = [ETFInDB(**e) for e in res.json()]
        common_assertions(res=res, assets=etfs_in_db, filters=params)

    @pytest.mark.parametrize(
        "filters, parameters, status_code",
        (
                ("ticker", ["INVALID"], 404),
                ("currency", -1, 404),
                ("family", "invalid", 404),
                ("exchange", ["CAC", "FLO"], 404)
        ),
    )
    async def test_invalid_input_raises_error(self, app: FastAPI, authorized_client: AsyncClient, filters: str,
                                              parameters: List[str], status_code: int) -> None:
        params = {filters: parameters}
        res = await authorized_client.get(app.url_path_for("screener:get-ETFs"), params=params)
        assert res.status_code == status_code


class TestGetFund:
    @pytest.mark.parametrize(
        "filters, num_filters",
        (
                (["family"], 4),
                (["ticker"], 3),
                (["currency"], 2),
                (["category"], 1),
                (["category", "family"], 1),
                (["exchange"], 1),
                (["market"], 2),
                ([], 1)
        ),
    )
    async def test_valid_filter_gets_funds(
            self, app: FastAPI, authorized_client: AsyncClient, test_funds: List[FundInDB], filters: List[str],
            num_filters: int) -> None:

        params = get_params(assets=test_funds, filters=filters, num_filters=num_filters)

        res = await authorized_client.get(app.url_path_for("screener:get-funds"), params=params)

        funds_in_db = [FundInDB(**e) for e in res.json()]
        common_assertions(res=res, assets=funds_in_db, filters=params)

    @pytest.mark.parametrize(
        "filters, parameters, status_code",
        (
                ("ticker", ["INVALID"], 404),
                ("currency", -1, 404),
                ("family", "invalid", 404),
                ("exchange", ["CAC", "FLO"], 404)
        ),
    )
    async def test_invalid_input_raises_error(self, app: FastAPI, authorized_client: AsyncClient, filters: str,
                                              parameters: List[str], status_code: int) -> None:
        params = {filters: parameters}
        res = await authorized_client.get(app.url_path_for("screener:get-funds"), params=params)
        assert res.status_code == status_code












