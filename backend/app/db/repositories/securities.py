from typing import List, Optional, Dict
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningInDB
from app.models.security import EquityCreate, EquityInDB, SecurityInDB
import pdb
import yfinance as yf

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

    async def add_tickers(self, *, new_tickers: List[str]) -> List[SecurityInDB]:

        added_tickers = []
        invalid_tickers = []

        # 1. GET tickers that are already included in database
        already_added_tickers = await self.get_securities_by_ticker(tickers=new_tickers)
        # 2. If there are no tickers in the database (previous function call returns None), assign to empty list
        # Otherwise, use list comprehension to get List[str] of tickers from List[SecurityInDB] returned from previous
        # function call
        already_added_tickers = (lambda x: [] if x is None else [t.ticker for t in x])(already_added_tickers)
        # 3. So we can use another list comprehension to only loop/POST new tickers avoid violating unique constraint

        for ticker in [tickers for tickers in new_tickers if tickers not in already_added_tickers]:
            try:
                data = yf.Ticker(ticker).info
            except:
                invalid_tickers.append(ticker)
                continue

            if data['quoteType'] == 'EQUITY':
                equity = await self._add_equity(new_equity=EquityCreate(ticker=ticker, name=data['shortName'],
                                                                        country=data['country'],
                                                                        summary=data['longBusinessSummary'],
                                                                        sector=data['sector'],
                                                                        industry=data['industry'],
                                                                        exchange=data['exchange']))
                added_tickers.append(SecurityInDB(**equity.dict(), type='Equity'))

        return added_tickers

    async def _add_equity(self, *, new_equity: EquityCreate) -> EquityInDB:
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
