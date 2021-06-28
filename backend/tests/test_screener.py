import random
from typing import List, Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from app.models.equity import EquityInDB

# decorate all tests with @pytest.mark.asyncio

pytestmark = pytest.mark.asyncio



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
            self, app: FastAPI, authorized_client: AsyncClient, test_equities1: List[EquityInDB], filters: List[str],
            num_filters: int) -> None:

        params = self.get_params(equities=test_equities1, filters=filters, num_filters=num_filters)

        res = await authorized_client.get(app.url_path_for("screener:get-equities"), params=params)

        equities_in_db = [EquityInDB(**e) for e in res.json()]
        self.common_assertions(res=res, equities=equities_in_db, filters=params)


    @pytest.mark.parametrize(
        "filters, parameters, status_code",
        (
                ("tickers", ["INVALID"], 404),
                ("countries", -1, 404),
                ("sectors", "invalid", 404),
                ("exchanges", ["CAC", "FLO"], 404)
        ),
    )
    async def test_invalid_input_raises_error(self, app: FastAPI, authorized_client: AsyncClient, filters: str,
                                              parameters: List[str], status_code: int) -> None:
        params = {filters: parameters}
        res = await authorized_client.get(app.url_path_for("screener:get-equities"), params=params)
        assert res.status_code == status_code

    @staticmethod
    def common_assertions(res, equities: List[EquityInDB], filters: Dict):
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        assert TestGetEquity.equities_meet_filter(equities=equities, filters=filters)

    @staticmethod
    def equities_meet_filter(equities: List[EquityInDB], filters: Dict):
        for equity in equities:
            for filter in filters.keys():
                if getattr(equity, filter) not in filters[filter]:
                    return False
        return True

    @staticmethod
    def get_params(equities, filters, num_filters):
        params = {key:[] for key in filters}
        for equity in random.sample(equities, num_filters):
            for filter in filters:
                params[filter].append(getattr(equity, filter))
        return params

class TestGetETF:
    async def test_valid_request_gets_etfs(
            self, app: FastAPI, authorized_client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        params = {'tickers': [test_equities1[0].ticker, test_equities1[1].ticker]}
        res = await authorized_client.get(app.url_path_for("screener:get-equities"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in test_equities1[0:2])
# TODO: More tests

# class TestGetETF:
#     async def test_valid_ticker_filter_gets_equities(
#             self, app: FastAPI, authorized_client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
#         params = {'tickers': [test_equities1[0].ticker, test_equities1[1].ticker]}
#         res = await authorized_client.get(app.url_path_for("equities:get-equities"), params=params)
#         assert res.status_code == HTTP_200_OK
#         assert isinstance(res.json(), list)
#         assert len(res.json()) > 0
#         equities_in_db = [EquityInDB(**e) for e in res.json()]
#
#         assert all(equity in equities_in_db for equity in test_equities1[0:2])
