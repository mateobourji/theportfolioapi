import logging
from typing import List, Optional

from app.db.repositories.base import BaseRepository
from app.models.equity import EquityQueryParams, EquityPublic
from app.models.etf import ETFQueryParams, ETFPublic

db_logger = logging.getLogger("DB")

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

        db_logger.log(level=logging.INFO,
                      msg="Querying ETFs Table with the following filters: %s" % vars(params))

        etfs = await self.db.fetch_all(query=GET_ETFs_QUERY, values=vars(params))

        if not etfs:
            db_logger.log(level=logging.INFO,
                          msg="No securities found in the ETFS Table with the following filters: %s" % (vars(params)))
            return None

        return [ETFPublic(**etf) for etf in etfs]
