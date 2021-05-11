from typing import List, Optional, Dict
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningInDB
from app.models.security import EquityCreate, EquityInDB, SecurityInDB, SecuritiesAddedToDB, InvalidTickers, \
    SecuritiesAlreadyInDB, POSTTickerResponse
import pdb
import yfinance as yf
import numpy as np

ADD_EQUITY_QUERY = """
    INSERT INTO equities (ticker, name, country, sector, industry, exchange)
    VALUES (:ticker, :name, :country, :sector, :industry, :exchange)
    RETURNING ticker, name, country, sector, industry, exchange;
"""

GET_SECURITIES_QUERY = """
    SELECT ticker, type 
    FROM securities
    WHERE ticker = ANY(:tickers);
    """

GET_ALL_SECURITIES_QUERY = """
    SELECT ticker, type
    FROM securities;
    """


class SecuritiesRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def add_tickers(self, *, new_tickers: List[str]) -> POSTTickerResponse:

        added_tickers = SecuritiesAddedToDB(securities=[])
        invalid_tickers = InvalidTickers(tickers=[])
        existing_tickers = SecuritiesAlreadyInDB(securities=[])

        # GET tickers that are already existing in database. If there are no existing tickers in the db, GET function
        # returns None. Therefore use lambda function to replace None with empty List to satisfy data validation.
        existing_tickers.securities = (lambda x: [] if x is None else x) \
            (await self.get_securities_by_ticker(tickers=new_tickers))

        for ticker in list(np.setdiff1d(new_tickers, [t.ticker for t in existing_tickers.securities])):

            try:
                data = yf.Ticker(ticker).info
                quote_type = data['quoteType']
            except:

                invalid_tickers.tickers.append(ticker)
                continue

            if quote_type == 'EQUITY':
                await self._add_equity(new_equity=EquityCreate(ticker=ticker, name=data['shortName'],
                                                               country=data['country'],
                                                               sector=data['sector'], industry=data['industry'],
                                                               exchange=data['exchange']))

                added_tickers.securities.append(SecurityInDB(ticker=ticker, type='Equity'))

        return POSTTickerResponse(added_tickers=added_tickers, existing_tickers=existing_tickers,
                                  invalid_tickers=invalid_tickers)

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
