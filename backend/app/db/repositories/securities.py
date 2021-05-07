from typing import List, Optional
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningInDB
from app.models.security import EquityCreate, EquityInDB, SecurityInDB
import pdb

ADD_EQUITY_QUERY = """
    INSERT INTO equities (ticker, name, country, summary, sector, industry, exchange)
    VALUES (:ticker, :name, :country, :summary, :sector, :industry, :exchange)
    RETURNING id, ticker, name, country, summary, sector, industry, exchange;
"""

GET_SECURITIES_QUERY = """
    SELECT id, ticker, type 
    FROM securities
    WHERE ticker = ANY(:tickers);
    """

GET_ALL_SECURITIES_QUERY = """
    SELECT id, ticker, type
    FROM securities;
    """

class SecuritiesRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def add_equity(self, *, new_equity: EquityCreate) -> EquityInDB:
        query_values = new_equity.dict()


        equity = await self.db.fetch_one(query=ADD_EQUITY_QUERY, values=query_values)

        return EquityInDB(**equity)

    async def get_securities_by_ticker(self, *, tickers: List[str]) -> Optional[List[SecurityInDB]]:
        query_values = {'tickers': tuple(tickers)}

        securities = await self.db.fetch_all(query=GET_SECURITIES_QUERY, values=query_values)

        if not securities:
            return None

        return [SecurityInDB(**s) for s in securities]

    async def get_all_securities(self) -> Optional[List[SecurityInDB]]:

        securities = await self.db.fetch_all(query=GET_ALL_SECURITIES_QUERY)

        if not securities:
            return None

        return [SecurityInDB(**s) for s in securities]
