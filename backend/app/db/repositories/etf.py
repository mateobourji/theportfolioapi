from typing import List, Optional

from app.db.repositories.base import BaseRepository
from app.models.equity import EquityQueryParams, EquityPublic
from app.models.etf import ETFQueryParams, ETFPublic

GET_ETFs_QUERY = """
    SELECT ticker, short_name, long_name, summary, currency, category, family, exchange, market
    FROM etfs
    WHERE 
        ((ticker = ANY(:ticker)) OR (:ticker IS NULL))
        AND ((long_name ILIKE ANY(:long_name)) OR (:long_name IS NULL))
        AND ((currency = ANY(:currency)) OR (:currency IS NULL))
        AND ((category = ANY(:category)) OR (:category IS NULL))
        AND ((family = ANY(:family)) OR (:family IS NULL))
        AND ((exchange = ANY(:exchange)) OR (:exchange IS NULL))
        AND ((market = ANY(:market)) OR (:market IS NULL)) 
    ORDER BY ticker asc;
    """

class ETFRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def get_etf(self, *, params: ETFQueryParams) -> Optional[List[ETFPublic]]:

        etfs = await self.db.fetch_all(query=GET_ETFs_QUERY, values=vars(params))

        if not etfs:
            return None

        return [ETFPublic(**etf) for etf in etfs]
