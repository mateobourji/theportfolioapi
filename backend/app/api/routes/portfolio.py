from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from app.core.external_data_interface import Financial_Data
import datetime
from app.core.check_tickers import check_tickers
from app.db.repositories.portfolio import PortfoliosRepository
from app.core.portfolio import Portfolio
from app.models.user import UserInDB
from app.models.portfolio import PortfolioCreate, PortfolioInDB, PortfolioPublic, PortfolioPOSTBodyParams
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
import json

router = APIRouter()


# @router.get("/", name="data:download-portfolio", status_code=HTTP_200_OK, response_model=PortfolioPublic)
# async def return_opt_portfolio(q: List[str] = Query(..., title="List of securities", min_length=2),
#                                start: Optional[datetime.date] = "2000-01-01",
#                                end: Optional[datetime.date] = datetime.date.today()) -> PortfolioPublic:
#     check_tickers(q)
#     portfolio = Portfolio(securities=q, start=start, end=end)
#
#     return PortfolioPublic(**portfolio.optimal_portfolio())


@router.post("/", name="portfolio:post", status_code=HTTP_200_OK, response_model=PortfolioPublic)
async def post_portfolio(params: PortfolioPOSTBodyParams,
                         current_user: UserInDB = Depends(get_current_active_user),
                         portfolio_repo: PortfoliosRepository = Depends(get_repository(PortfoliosRepository))
                         ) -> PortfolioPublic:

    check_tickers(params.securities)
    optimal_portfolio = Portfolio(**params.dict()).optimal_portfolio()
    new_portfolio = PortfolioCreate(user_id=current_user.id, **optimal_portfolio)
    portfolio = await portfolio_repo.add_portfolio(new_portfolio=new_portfolio)

    return PortfolioPublic(**portfolio.dict())
