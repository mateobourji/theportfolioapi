from typing import List, Optional

from app.db.repositories.base import BaseRepository
from app.models.equity import EquityQueryParams, EquityPublic
from app.models.etf import ETFQueryParams, ETFPublic

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

class EquityRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def get_equities(self, *, params: EquityQueryParams) -> Optional[List[EquityPublic]]:

        equities = await self.db.fetch_all(query=GET_EQUITIES_QUERY, values=vars(params))

        if not equities:
            return None

        return [EquityPublic(**e) for e in equities]


