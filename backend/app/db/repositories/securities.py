from typing import List, Optional, Dict
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from app.db.repositories.base import BaseRepository
from app.models.security import EquityCreate, EquityInDB, SecurityInDB, SecuritiesAddedToDB, InvalidTickers, \
    SecuritiesAlreadyInDB, POSTTickerResponse
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

GET_EQUITIES_QUERY = """
    SELECT ticker, name, country, sector, industry, exchange
    FROM equities
    WHERE 
        ((ticker = ANY(:tickers)) OR (:tickers IS NULL))
        AND ((name ILIKE ANY(:names)) OR (:names IS NULL))
        AND ((sector = ANY(:sectors)) OR (:sectors IS NULL))
        AND ((industry = ANY(:industries)) OR (:industries IS NULL))
        AND ((country = ANY(:countries)) OR (:countries IS NULL))
        AND ((exchange = ANY(:exchanges)) OR (:exchanges IS NULL));
    """

GET_ALL_EQUITIES_QUERY = """
    SELECT ticker, name, country, sector, industry, exchange
    FROM equities
    """


class SecuritiesRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def add_tickers(self, *, tickers: List[str]) -> POSTTickerResponse:

        added_tickers = SecuritiesAddedToDB(securities=[])
        invalid_tickers = InvalidTickers(tickers=[])
        existing_tickers = SecuritiesAlreadyInDB(securities=[])

        # GET tickers that are already existing in database. If there are no existing tickers in the db, GET function
        # returns None. Therefore use lambda function to replace None with empty List to satisfy data validation.
        existing_tickers.securities = (lambda x: [] if x is None else x) \
            (await self.get_securities_by_ticker(tickers=tickers))

        for ticker in list(np.setdiff1d(tickers, [t.ticker for t in existing_tickers.securities])):

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

    async def get_equities_by_ticker(self, *, tickers: Optional[List[str]] = None, names: Optional[List[str]] = None,
                                     sectors: Optional[List[str]] = None, industries: Optional[List[str]] = None,
                                     countries: Optional[List[str]] = None, exchanges: Optional[List[str]] = None
                                     ) -> Optional[List[EquityInDB]]:

        #Optional WHERE IN ANY() SQL query above requires tuple of values to filter, or NULL/None to ignore filter
        #Lambda function below returns tuple if list is passed, otherwise None
        tuple_or_none = (lambda x: tuple(x) if x is not None else x)
        query_values = {'tickers': tuple_or_none(tickers), 'names': tuple_or_none(names),
                        'sectors': tuple_or_none(sectors), 'industries': tuple_or_none(industries),
                        'countries': tuple_or_none(countries), 'exchanges': tuple_or_none(exchanges)}

        equities = await self.db.fetch_all(query=GET_EQUITIES_QUERY, values=query_values)

        if not equities:
            return None

        return [EquityInDB(**e) for e in equities]

    async def get_all_equities(self) -> Optional[List[EquityInDB]]:

        equities = await self.db.fetch_all(query=GET_ALL_EQUITIES_QUERY)

        if not equities:
            return None

        return [EquityInDB(**e) for e in equities]
