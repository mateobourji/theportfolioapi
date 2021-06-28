from typing import List, Optional
from app.db.repositories.base import BaseRepository
from app.models.ticker import TickerPublic
from app.models.equity import EquityCreate, EquityInDB, EquityQueryParams, EquityPublic
from app.models.etf import ETFCreate, ETFInDB, ETFQueryParams, ETFPublic
import numpy as np
from app.core.external_data_interface import Ticker_Data

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
    RETURNING ticker, name, exchange, bond_position, investment_grade_bonds, 
    junk_bonds, stock_position, real_estate, consumer_cyclical, basic_materials, consumer_defensive, technology,
    communication_services, financial_services, utilities, industrials, energy, healthcare;
    """

GET_EQUITIES_QUERY = """
    SELECT ticker, short_name, long_name, summary, currency, sector, industry, exchange, market, country, city
    FROM equities
    WHERE 
        ((ticker = ANY(:ticker)) OR (:ticker IS NULL))
        AND ((long_name ILIKE ANY(:long_name)) OR (:long_name IS NULL))
        AND ((currency = ANY(:currency)) OR (:currency IS NULL))
        AND ((sector = ANY(:sector)) OR (:sector IS NULL))
        AND ((industry = ANY(:industry)) OR (:industry IS NULL))
        AND ((exchange = ANY(:exchange)) OR (:exchange IS NULL))
        AND ((market = ANY(:market)) OR (:market IS NULL))
        AND ((country = ANY(:country)) OR (:country IS NULL))
        AND ((city = ANY(:city)) OR (:city IS NULL))
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
        AND ((bond_position >= :min_bond) OR (:min_bond IS NULL))
        AND ((stock_position >= :min_stock) OR (:min_stock IS NULL))
        AND ((investment_grade_bonds >= :min_investment_grade) OR (:min_investment_grade IS NULL))
        AND ((investment_grade_bonds <= :max_investment_grade) OR (:max_investment_grade IS NULL))
        AND ((junk_bonds >= :min_junk_bonds) OR (:min_junk_bonds IS NULL))
        AND ((junk_bonds <= :max_junk_bonds) OR (:max_junk_bonds IS NULL))
        AND ((real_estate >= :min_real_estate) OR (:min_real_estate IS NULL))
        AND ((real_estate <= :max_real_estate) OR (:max_real_estate IS NULL))
        AND ((consumer_cyclical >= :min_consumer_cyclical) OR (:min_consumer_cyclical IS NULL))
        AND ((consumer_cyclical <= :max_consumer_cyclical) OR (:max_consumer_cyclical IS NULL))
        AND ((basic_materials >= :min_basic_materials) OR (:min_basic_materials IS NULL))
        AND ((basic_materials <= :max_basic_materials) OR (:max_basic_materials IS NULL))
        AND ((consumer_defensive >= :min_consumer_defensive) OR (:min_consumer_defensive IS NULL))
        AND ((consumer_defensive <= :max_consumer_defensive) OR (:max_consumer_defensive IS NULL))
        AND ((technology >= :min_technology) OR (:min_technology IS NULL))
        AND ((technology <= :max_technology) OR (:max_technology IS NULL))
        AND ((communication_services >= :min_communication_services) OR (:min_communication_services IS NULL))
        AND ((communication_services <= :max_communication_services) OR (:max_communication_services IS NULL))
        AND ((financial_services >= :min_financial_services) OR (:min_financial_services IS NULL))
        AND ((financial_services <= :max_financial_services) OR (:max_financial_services IS NULL))
        AND ((utilities >= :min_utilities) OR (:min_utilities IS NULL))
        AND ((utilities <= :max_utilities) OR (:max_utilities IS NULL))
        AND ((industrials >= :min_industrials) OR (:min_industrials IS NULL))
        AND ((industrials <= :max_industrials) OR (:max_industrials IS NULL))
        AND ((energy >= :min_energy) OR (:min_energy IS NULL))
        AND ((energy <= :max_energy) OR (:max_energy IS NULL))
        AND ((healthcare >= :min_healthcare) OR (:min_healthcare IS NULL))
        AND ((healthcare <= :max_healthcare) OR (:max_healthcare IS NULL))
    ORDER BY ticker asc;
    """


class SecuritiesRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def get_equities_by_ticker(self, *, params: EquityQueryParams) -> Optional[List[EquityPublic]]:

        equities = await self.db.fetch_all(query=GET_EQUITIES_QUERY, values=vars(params))

        if not equities:
            return None

        return [EquityPublic(**e) for e in equities]

    async def get_securities_by_ticker(self, *, tickers: List[str]) -> Optional[List[TickerPublic]]:
        # Optional WHERE IN ANY() SQL query above requires tuple of values to filter, or NULL/None to ignore filter
        # Lambda function below returns tuple if list is passed, otherwise None
        query_values = {'tickers': (lambda x: tuple(x) if x is not None else x)(tickers)}

        securities = await self.db.fetch_all(query=GET_SECURITIES_QUERY, values=query_values)

        if not securities:
            return None

        return [TickerPublic(**s) for s in securities]

    async def get_etf(self, *, params: ETFQueryParams) -> Optional[List[ETFPublic]]:

        etfs = await self.db.fetch_all(query=GET_ETFS_QUERY, values=vars(params))

        if not etfs:
            return None

        return [ETFPublic(**etf) for etf in etfs]
