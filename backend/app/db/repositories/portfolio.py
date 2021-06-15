from typing import List, Optional
from app.db.repositories.base import BaseRepository
from app.models.portfolio import PortfolioCreate, PortfolioInDB
from app.core.portfolio import Portfolio

ADD_PORTFOLIO_QUERY = """
    INSERT INTO portfolios (user_id, portfolio_weights, returns, std, sharpe_ratio, return_over_risk, 
    optimization_type, optimization_method)
    VALUES (:user_id, :portfolio_weights, :returns, :std, :sharpe_ratio, :return_over_risk, 
    :optimization_type, :optimization_method)
    RETURNING id, user_id, portfolio_weights, returns, std, sharpe_ratio, return_over_risk, 
    optimization_type, optimization_method, added_at, updated_at;
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




class PortfoliosRepository(BaseRepository):
    """"
    All database actions associated with the Ticker resource
    """

    async def add_portfolio(self, *, new_portfolio: PortfolioCreate) -> PortfolioInDB:

        portfolio = await self.db.fetch_one(query=ADD_PORTFOLIO_QUERY, values=vars(new_portfolio))

        return PortfolioInDB(**portfolio)