import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from app.models.security import SecurityCreate, SecurityInDB, SecurityBase, EquityInDB
from typing import List, Union


class TestGetSecurity:
    async def test_valid_input_gets_ticker(
            self, app: FastAPI, client: AsyncClient, test_equity1: EquityInDB, test_equity2: EquityInDB) -> None:
        params = {'key1': test_equity1.ticker, 'key2': test_equity2.ticker}
        res = await client.get(app.url_path_for("securities:get-securities-by-ticker"), params=params)
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        securities = [SecurityInDB(**s) for s in res.json()]
        test_security1 = SecurityInDB(**test_equity1.dict())
        test_security2 = SecurityInDB(**test_equity2.dict())
        assert test_security1 in securities
        assert test_security2 in securities

if __name__ = '__main__':
