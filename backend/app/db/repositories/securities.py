from typing import List, Optional, Dict
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from app.db.repositories.base import BaseRepository
from app.models.security import SecurityInDB, SecuritiesAddedToDB, InvalidTickers, SecuritiesAlreadyInDB, \
    POSTTickerResponse
from app.models.equity import EquityCreate, EquityInDB
from app.models.etf import ETFCreate, ETFInDB, ETFQueryParams
import yfinance as yf
import yahooquery as yq
import numpy as np

ADD_EQUITY_QUERY = """
    INSERT INTO equities (ticker, name, country, sector, industry, exchange)
    VALUES (:ticker, :name, :country, :sector, :industry, :exchange)
    RETURNING ticker, name, country, sector, industry, exchange;
    """

ADD_ETF_QUERY = """
    INSERT INTO etfs (ticker, name, exchange, bond_position, investment_grade_bonds, 
    junk_bonds, stock_position, real_estate, consumer_cyclical, basic_materials, consumer_defensive, technology, 
    communication_services, financial_services, utilities, industrials, energy, healthcare)
    VALUES (:ticker, :name, :exchange, :bond_position, :investment_grade_bonds, 
    :junk_bonds, :stock_position, :real_estate, :consumer_cyclical, :basic_materials, :consumer_defensive, :technology,
     :communication_services, :financial_services, :utilities, :industrials, :energy, :healthcare)
    RETURNING ticker, name, exchange, bond_position, bond_maturity, bond_duration, investment_grade_bonds, 
    junk_bonds, stock_position, real_estate, consumer_cyclical, basic_materials, consumer_defensive, technology,
    communication_services, financial_services, utilities, industrials, energy, healthcare;
    """

GET_SECURITIES_QUERY = """
    SELECT ticker, type 
    FROM securities
    WHERE ((ticker = ANY(:tickers)) OR (:tickers IS NULL))
    ORDER BY ticker asc;
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
        AND ((exchange = ANY(:exchanges)) OR (:exchanges IS NULL))
    ORDER BY ticker asc;
    """

GET_ETFS_QUERY = """
    SELECT ticker, name, exchange, bond_position, investment_grade_bonds, 
    junk_bonds, stock_position, real_estate, consumer_cyclical, basic_materials, consumer_defensive, technology, 
    communication_services, financial_services, utilities, industrials, energy, healthcare
    FROM etfs
    WHERE 
        ((ticker = ANY(:tickers)) OR (:tickers IS NULL))
        AND ((name ILIKE ANY(:names)) OR (:names IS NULL))
        AND ((exchange = ANY(:exchanges)) OR (:exchanges IS NULL))
        AND ((bond_position > :min_bond) OR (:min_bond IS NULL))
        AND ((stock_position > :min_stock) OR (:min_stock IS NULL))
        AND ((investment_grade_bonds > :min_investment_grade) OR (:min_investment_grade IS NULL))
        AND ((investment_grade_bonds < :max_investment_grade) OR (:max_investment_grade IS NULL))
        AND ((junk_bonds > :min_junk_bonds) OR (:min_junk_bonds IS NULL))
        AND ((junk_bonds < :max_junk_bonds) OR (:max_junk_bonds IS NULL))
        AND ((real_estate > :min_real_estate) OR (:min_real_estate IS NULL))
        AND ((real_estate < :max_real_estate) OR (:max_real_estate IS NULL))
        AND ((consumer_cyclical > :min_consumer_cyclical) OR (:min_consumer_cyclical IS NULL))
        AND ((consumer_cyclical < :max_consumer_cyclical) OR (:max_consumer_cyclical IS NULL))
        AND ((basic_materials > :min_basic_materials) OR (:min_basic_materials IS NULL))
        AND ((basic_materials < :max_basic_materials) OR (:max_basic_materials IS NULL))
        AND ((consumer_defensive > :min_consumer_defensive) OR (:min_consumer_defensive IS NULL))
        AND ((consumer_defensive < :max_consumer_defensive) OR (:max_consumer_defensive IS NULL))
        AND ((technology > :min_technology) OR (:min_technology IS NULL))
        AND ((technology < :max_technology) OR (:max_technology IS NULL))
        AND ((communication_services > :min_communication_services) OR (:min_communication_services IS NULL))
        AND ((communication_services < :max_communication_services) OR (:max_communication_services IS NULL))
        AND ((financial_services > :min_financial_services) OR (:min_financial_services IS NULL))
        AND ((financial_services < :max_financial_services) OR (:max_financial_services IS NULL))
        AND ((utilities > :min_utilities) OR (:min_utilities IS NULL))
        AND ((utilities < :max_utilities) OR (:max_utilities IS NULL))
        AND ((industrials > :min_industrials) OR (:min_industrials IS NULL))
        AND ((industrials < :max_industrials) OR (:max_industrials IS NULL))
        AND ((energy > :min_energy) OR (:min_energy IS NULL))
        AND ((energy < :max_energy) OR (:max_energy IS NULL))
        AND ((healthcare > :min_healthcare) OR (:min_healthcare IS NULL))
        AND ((healthcare < :max_healthcare) OR (:max_healthcare IS NULL))
    ORDER BY ticker asc;
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
                data = yq.Ticker(ticker)
                quote_type = data.quote_type[ticker.upper()]['quoteType']
            except:

                invalid_tickers.tickers.append(ticker)
                continue

            if quote_type == 'EQUITY':
                await self._add_equity(new_equity=EquityCreate(ticker=ticker,
                                                               name=data.quote_type[ticker.upper()]['shortName'],
                                                               country=data.summary_profile[ticker.upper()]['country'],
                                                               sector=data.summary_profile[ticker.upper()]['sector'],
                                                               industry=data.summary_profile[ticker.upper()][
                                                                   'industry'],
                                                               exchange=data.quote_type[ticker.upper()]['exchange']))

                added_tickers.securities.append(SecurityInDB(ticker=ticker, type='Equity'))

            if quote_type == 'ETF':
                await self._add_etf(new_ETF=ETFCreate(ticker=ticker,
                                                      name=data.quote_type[ticker.upper()]['shortName'],
                                                      exchange=data.quote_type[ticker.upper()]['exchange'],
                                                      bond_position=(1 - data.fund_category_holdings.iloc[0, 1]),
                                                      investment_grade_bonds=data.fund_bond_ratings.iloc[0, 0]
                                                                             + data.fund_bond_ratings.iloc[1, 0]
                                                                             + data.fund_bond_ratings.iloc[2, 0]
                                                                             + data.fund_bond_ratings.iloc[3, 0]
                                                                             + data.fund_bond_ratings.iloc[6, 0],
                                                      junk_bonds=data.fund_bond_ratings.iloc[4, 0]
                                                                 + data.fund_bond_ratings.iloc[5, 0]
                                                                 + data.fund_bond_ratings.iloc[7, 0]
                                                                 + data.fund_bond_ratings.iloc[8, 0],
                                                      stock_position=data.fund_category_holdings.iloc[0, 1],
                                                      real_estate=data.fund_sector_weightings.iloc[0, 0],
                                                      consumer_cyclical=data.fund_sector_weightings.iloc[1, 0],
                                                      basic_materials=data.fund_sector_weightings.iloc[2, 0],
                                                      consumer_defensive=data.fund_sector_weightings.iloc[3, 0],
                                                      technology=data.fund_sector_weightings.iloc[4, 0],
                                                      communication_services=data.fund_sector_weightings.iloc[5, 0],
                                                      financial_services=data.fund_sector_weightings.iloc[6, 0],
                                                      utilities=data.fund_sector_weightings.iloc[7, 0],
                                                      industrials=data.fund_sector_weightings.iloc[8, 0],
                                                      energy=data.fund_sector_weightings.iloc[9, 0],
                                                      healthcare=data.fund_sector_weightings.iloc[10, 0]))

                added_tickers.securities.append(SecurityInDB(ticker=ticker, type='ETF'))

        return POSTTickerResponse(added_tickers=added_tickers, existing_tickers=existing_tickers,
                                  invalid_tickers=invalid_tickers)

    async def _add_equity(self, *, new_equity: EquityCreate) -> EquityInDB:
        query_values = new_equity.dict()

        equity = await self.db.fetch_one(query=ADD_EQUITY_QUERY, values=query_values)

        return EquityInDB(**equity)

    async def _add_etf(self, *, new_ETF: ETFCreate) -> ETFInDB:
        query_values = new_ETF.dict()

        etf = await self.db.fetch_one(query=ADD_ETF_QUERY, values=query_values)

        return ETFInDB(**etf)

    async def get_equities_by_ticker(self, *, tickers: Optional[List[str]] = None, names: Optional[List[str]] = None,
                                     sectors: Optional[List[str]] = None, industries: Optional[List[str]] = None,
                                     countries: Optional[List[str]] = None, exchanges: Optional[List[str]] = None
                                     ) -> Optional[List[EquityInDB]]:

        # Optional WHERE IN ANY() SQL query above requires tuple of values to filter, or NULL/None to ignore filter
        # Lambda function below returns tuple if list is passed, otherwise None
        tuple_or_none = (lambda x: tuple(x) if x is not None else x)
        query_values = {'tickers': tuple_or_none(tickers), 'names': tuple_or_none(names),
                        'sectors': tuple_or_none(sectors), 'industries': tuple_or_none(industries),
                        'countries': tuple_or_none(countries), 'exchanges': tuple_or_none(exchanges)}

        equities = await self.db.fetch_all(query=GET_EQUITIES_QUERY, values=query_values)

        if not equities:
            return None

        return [EquityInDB(**e) for e in equities]

    async def get_securities_by_ticker(self, *, tickers: List[str]) -> Optional[List[SecurityInDB]]:
        # Optional WHERE IN ANY() SQL query above requires tuple of values to filter, or NULL/None to ignore filter
        # Lambda function below returns tuple if list is passed, otherwise None
        query_values = {'tickers': (lambda x: tuple(x) if x is not None else x)(tickers)}

        securities = await self.db.fetch_all(query=GET_SECURITIES_QUERY, values=query_values)

        if not securities:
            return None

        return [SecurityInDB(**s) for s in securities]

    async def get_etf(self, *, params: ETFQueryParams) -> Optional[List[ETFInDB]]:

        # Optional WHERE IN ANY() SQL query above requires tuple of values to filter, or NULL/None to ignore filter
        # Lambda function below returns tuple if list is passed, otherwise None

        query_values = {'tickers': params.tickers, 'names': params.names, 'exchanges': params.exchanges,
                        'min_bond': params.min_bond, 'min_investment_grade': params.min_investment_grade,
                        'max_investment_grade': params.max_investment_grade, 'min_junk_bonds': params.min_junk_bonds,
                        'max_junk_bonds': params.max_junk_bonds, 'min_real_estate': params.min_real_estate,
                        'max_real_estate': params.max_real_estate, 
                        'min_consumer_cyclical': params.min_consumer_cyclical,
                        'max_consumer_cyclical': params.max_consumer_cyclical, 
                        'min_basic_materials': params.min_basic_materials, 
                        'max_basic_materials': params.max_basic_materials, 
                        'min_consumer_defensive': params.min_consumer_defensive,
                        'max_consumer_defensive': params.max_consumer_defensive,
                        'min_technology': params.min_technology, 'max_technology': params.max_technology,
                        'min_communication_services': params.min_communication_services, 
                        'max_communication_services': params.max_communication_services,
                        'min_financial_services': params.min_financial_services,
                        'max_financial_services': params.max_financial_services,
                        'min_utilities': params.min_utilities, 'max_utilities': params.max_utilities,
                        'min_industrials': params.min_industrials, 'max_industrials': params.max_industrials,
                        'min_energy': params.min_energy, 'max_energy': params.max_energy,
                        'min_healthcare': params.min_healthcare, 'max_healthcare': params.max_healthcare}

        etfs = await self.db.fetch_all(query=GET_ETFS_QUERY, values=query_values)

        if not etfs:
            return None

        return [ETFInDB(**etf) for etf in etfs]
