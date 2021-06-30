from typing import List, Optional

from app.db.repositories.base import BaseRepository
from app.models.fund import FundQueryParams, FundPublic

GET_FUNDS_QUERY = """
    SELECT ticker, short_name, long_name, summary, currency, category, family, exchange, market
    FROM funds
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


class FundRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def get_fund(self, *, params: FundQueryParams) -> Optional[List[FundPublic]]:
        funds = await self.db.fetch_all(query=GET_FUNDS_QUERY, values=vars(params))

        if not funds:
            return None

        return [FundPublic(**fund) for fund in funds]
