import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from app.models.security import SecurityInDB, SecurityBase, EquityInDB
from typing import List, Union

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture
def test_tickers():
    return ["AMZN", "AAPL"]


@pytest.fixture
def test_tickers2():
    return ["JNJ", "TSLA"]


@pytest.fixture
def test_tickers3():
    return ["AMZN", "GOOG"]

@pytest.fixture
def test_tickers4():
    """ETFs"""
    return ["BND"]


@pytest.fixture
def ticker_list():
    return ["AMZN", "AAPL"]


@pytest.fixture
def invalid_tickers():
    return ["JJJJ", "GGGA"]


@pytest.fixture()
def test_equities_ticker_filter():
    return ["CSCO", "NFLX"]



class TestTickersRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient, test_tickers: List[str]) -> None:
        res = await client.post(app.url_path_for("securities:add-tickers"), json=test_tickers)
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("securities:add-tickers"), json="INVALID")
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateTicker:
    async def test_valid_input_creates_ticker(self, app: FastAPI, client: AsyncClient, test_tickers2: List[str]
                                              ) -> None:
        res = await client.post(app.url_path_for("securities:add-tickers"), json=test_tickers2)
        assert res.status_code == HTTP_201_CREATED

        created_ticker = [ticker['ticker'] for ticker in res.json()['added_tickers']['securities']]
        assert created_ticker == test_tickers2

    async def test_valid_ETF_input_creates_ticker(self, app: FastAPI, client: AsyncClient, test_tickers4: List[str]
                                              ) -> None:
        res = await client.post(app.url_path_for("securities:add-tickers"), json=test_tickers4)
        assert res.status_code == HTTP_201_CREATED

        created_ticker = [ticker['ticker'] for ticker in res.json()['added_tickers']['securities']]

        assert created_ticker == test_tickers4

    async def test_repeated_input_returns_empty_list(self, app: FastAPI, client: AsyncClient, test_tickers2: List[str]
                                                     ) -> None:
        # If tickers are already in db, API should return empty list.
        res = await client.post(app.url_path_for("securities:add-tickers"), json=test_tickers2)
        assert res.status_code == HTTP_201_CREATED

        created_ticker = [ticker['ticker'] for ticker in res.json()['added_tickers']['securities']]
        assert created_ticker == []

    async def test_invalid_ticker(self, app: FastAPI, client: AsyncClient, invalid_tickers: List[str]) -> None:
        # If tickers are already in db, API should return empty list.
        res = await client.post(app.url_path_for("securities:add-tickers"), json=invalid_tickers)
        assert res.status_code == HTTP_201_CREATED

        returned_tickers = res.json()['invalid_tickers']['tickers']
        assert returned_tickers[::-1] == invalid_tickers

    async def test_partial_repeated_input_returns_partial_creation(self, app: FastAPI, client: AsyncClient,
                                                                   test_tickers3: List[str]) -> None:
        # If part of tickers already in db, API should return only newly created tickers not previously in db

        res = await client.post(app.url_path_for("securities:add-tickers"), json=test_tickers3)
        assert res.status_code == HTTP_201_CREATED

        created_ticker = [ticker['ticker'] for ticker in res.json()['added_tickers']['securities']]
        assert created_ticker == [test_tickers3[1]]

    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
                (None, 422),
                ({}, 422),
                (["AMZN", "INVALID"], 422),
                ("AMZN", 422),
                ({"name": "test_name", "description": "test"}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
            self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int
    ) -> None:
        res = await client.post(
            app.url_path_for("securities:add-tickers"), json={"new_ticker": invalid_payload}
        )
        assert res.status_code == status_code


class TestGetSecurity:
    # TODO: ticker_list based on tickers in conftest, not tickers added to db in previous tests
    async def test_valid_input_gets_ticker(
            self, app: FastAPI, client: AsyncClient, ticker_list: List[str]) -> None:
        params = {'q': [ticker_list[0], ticker_list[1]]}

        res = await client.get(app.url_path_for("securities:get-securities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        securities = [SecurityInDB(**s) for s in res.json()]
        test_security1 = SecurityInDB(ticker=ticker_list[0], type='equity')
        test_security2 = SecurityInDB(ticker=ticker_list[1], type='equity')
        assert test_security1 in securities
        assert test_security2 in securities

    @pytest.mark.parametrize(
        "invalid_ticker_list, status_code",
        (
                (["AAPL", "INVALID"], 404),
                (-1, 404),
                (None, 404),
        ),
    )
    async def test_invalid_input_raises_error(
            self, app: FastAPI, client: AsyncClient, invalid_ticker_list: List[str], status_code: int) -> None:
        params = {'q': ticker_list}

        res = await client.get(app.url_path_for("securities:get-securities-by-ticker"), params=params)
        assert res.status_code == status_code

    async def test_get_all_securities_returns_valid_response(
            self, app: FastAPI, client: AsyncClient, ticker_list: List[str]) -> None:
        res = await client.get(app.url_path_for("securities:get-all-securities"))
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        securities = [SecurityInDB(**s) for s in res.json()]
        test_security1 = SecurityInDB(ticker=ticker_list[0], type='equity')
        test_security2 = SecurityInDB(ticker=ticker_list[1], type='equity')
        assert test_security1 in securities
        assert test_security2 in securities


class TestGetEquity:
    async def test_valid_ticker_filter_gets_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        params = {'tickers': [test_equities1[0].ticker, test_equities1[1].ticker]}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in test_equities1[0:2])

    async def test_valid_country_filter_gets_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        country_filter = ["United Kingdom"]
        params = {'countries': country_filter}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in
                   [equity for equity in test_equities1 if equity.country in country_filter])

    async def test_valid_sector_filter_gets_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        sector_filter = ["Technology", "Consumer Cyclical"]
        params = {'sectors': sector_filter}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in
                   [equity for equity in test_equities1 if equity.sector in sector_filter])

    async def test_valid_industry_filter_gets_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        industry_filter = ["Entertainment", "Oil & Gas Integrated"]
        params = {'industry': industry_filter}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in
                   [equity for equity in test_equities1 if equity.industry in industry_filter])

    async def test_valid_exchange_filter_gets_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        exchange_filter = ["NMS"]
        params = {'exchange': exchange_filter}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in
                   [equity for equity in test_equities1 if equity.country in exchange_filter])

    async def test_valid_name_filter_gets_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        name_filter = ["Netflix, Inc."]
        params = {'name': name_filter}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in
                   [equity for equity in test_equities1 if equity.name in name_filter])

    async def test_valid_sector_and_industries_filters_gets_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
        sector_filter = ["Technology"]
        industry_filter = ["Communication Equipment"]
        params = {'sectors': sector_filter, 'industries': industry_filter}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in
                   [equity for equity in test_equities1 if equity.sector in sector_filter
                                                        if equity.industry in industry_filter])

    async def test_no_filters_gets_all_equities(
            self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:

        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"))
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        equities_in_db = [EquityInDB(**e) for e in res.json()]

        assert all(equity in equities_in_db for equity in test_equities1)

    @pytest.mark.parametrize(
        "filters, parameters, status_code",
        (
                ("tickers", ["INVALID"], 404),
                ("countries", -1, 404),
                ("sectors", "invalid", 404),
                ("exchanges", ["CAC", "FLO"], 404)
        ),
    )
    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient, filters: str,
                                              parameters: List[str], status_code: int) -> None:
        params = {filters: parameters}
        res = await client.get(app.url_path_for("equities:get-equities-by-ticker"), params=params)
        assert res.status_code == status_code

    # async def test_get_all_securities_returns_valid_response(
    #         self, app: FastAPI, client: AsyncClient, test_equities1: List[EquityInDB]) -> None:
    #     res = await client.get(app.url_path_for("equities:get-all-equities"))
    #     assert res.status_code == HTTP_200_OK
    #     assert isinstance(res.json(), list)
    #     assert len(res.json()) > 0
    #     equities = [EquityInDB(**e) for e in res.json()]
    #
    #     assert all(equity in equities for equity in test_equities1)

# class TestUpdateticker:
#     @pytest.mark.parametrize(
#         "attrs_to_change, values",
#         (
#                 (["name"], ["new fake ticker name"]),
#                 (["description"], ["new fake ticker description"]),
#                 (["price"], [3.14]),
#                 (["ticker_type"], ["full_clean"]),
#                 (["name", "description"], ["extra new fake ticker name", "extra new fake ticker description"]),
#                 (["price", "ticker_type"], [42.00, "dust_up"]),
#         ),
#     )
#     async def test_update_ticker_with_valid_input(
#             self,
#             app: FastAPI,
#             client: AsyncClient,
#             test_ticker: tickerInDB,
#             attrs_to_change: List[str],
#             values: List[str],
#     ) -> None:
#         ticker_update = {"ticker_update": {attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))}}
#         res = await client.put(
#             app.url_path_for("tickers:update-ticker-by-id", id=test_ticker.id),
#             json=ticker_update
#         )
#         assert res.status_code == HTTP_200_OK
#         updated_ticker = tickerInDB(**res.json())
#         assert updated_ticker.id == test_ticker.id  # make sure it's the same ticker
#         # make sure that any attribute we updated has changed to the correct value
#         for i in range(len(attrs_to_change)):
#             assert getattr(updated_ticker, attrs_to_change[i]) != getattr(test_ticker, attrs_to_change[i])
#             assert getattr(updated_ticker, attrs_to_change[i]) == values[i]
#         # make sure that no other attributes' values have changed
#         for attr, value in updated_ticker.dict().items():
#             if attr not in attrs_to_change:
#                 assert getattr(test_ticker, attr) == value
#
#     @pytest.mark.parametrize(
#         "id, payload, status_code",
#         (
#                 (-1, {"name": "test"}, 422),
#                 (0, {"name": "test2"}, 422),
#                 (500, {"name": "test3"}, 404),
#                 (1, None, 422),
#                 (1, {"ticker_type": "invalid ticker type"}, 422),
#                 (1, {"ticker_type": None}, 400),
#         ),
#     )
#     async def test_update_ticker_with_invalid_input_throws_error(
#             self,
#             app: FastAPI,
#             client: AsyncClient,
#             id: int,
#             payload: dict,
#             status_code: int,
#     ) -> None:
#         ticker_update = {"ticker_update": payload}
#         res = await client.put(
#             app.url_path_for("tickers:update-ticker-by-id", id=id),
#             json=ticker_update
#         )
#         assert res.status_code == status_code
#
#
# class TestDeleteticker:
#
#     async def test_can_delete_ticker_successfully(
#             self, app: FastAPI, client: AsyncClient, test_ticker: tickerInDB
#     ) -> None:
#         res = await client.delete(app.url_path_for("tickers:delete-ticker-by-id", id=test_ticker.id))
#         assert res.status_code == HTTP_200_OK
#         res = await client.get(app.url_path_for("tickers:get-ticker-by-id", id=test_ticker.id))
#         assert res.status_code == HTTP_404_NOT_FOUND
#
#     @pytest.mark.parametrize(
#         "id, status_code",
#         (
#                 (-1, 422),
#                 (500, 404),
#                 (None, 422),
#                 ("Invalid", 422)
#         )
#     )
#     async def test_delete_with_invalid_input_throws_error(
#             self, app: FastAPI, client: AsyncClient, id: int, status_code: int
#     ) -> None:
#         res = await client.delete(app.url_path_for("tickers:delete-ticker-by-id", id=id))
#         assert res.status_code == status_code
