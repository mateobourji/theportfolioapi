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


@router.post("/create", name="portfolio:post", status_code=HTTP_201_CREATED, response_model=PortfolioPublic)
async def post_portfolio(params: PortfolioPOSTBodyParams,
                         current_user: UserInDB = Depends(get_current_active_user),
                         portfolio_repo: PortfoliosRepository = Depends(get_repository(PortfoliosRepository))
                         ) -> PortfolioPublic:
    check_tickers(params.securities)
    optimal_portfolio = Portfolio(**params.dict()).optimal_portfolio()
    new_portfolio = PortfolioCreate(user_id=current_user.id, **optimal_portfolio)
    portfolio = await portfolio_repo.add_portfolio(new_portfolio=new_portfolio)

    return PortfolioPublic(**portfolio.dict())


@router.get("/all", name="portfolio:get-all", status_code=HTTP_200_OK, response_model=List[PortfolioPublic])
async def get_all_portfolios(current_user: UserInDB = Depends(get_current_active_user),
                               portfolio_repo: PortfoliosRepository = Depends(get_repository(PortfoliosRepository)
                                                                              )) -> List[PortfolioPublic]:
    portfolios = await portfolio_repo.get_all_portfolios(user_id=current_user.id)

    return [PortfolioPublic(**portfolio.dict()) for portfolio in portfolios]


@router.get("/{portfolio_id}", name="portfolio:get-by-id", status_code=HTTP_200_OK, response_model=PortfolioPublic)
async def get_portfolio_by_id(portfolio_id: int,
                               current_user: UserInDB = Depends(get_current_active_user),
                               portfolio_repo: PortfoliosRepository = Depends(get_repository(PortfoliosRepository)
                                                                              )) -> PortfolioPublic:
    portfolio = await portfolio_repo.get_portfolio_by_id(user_id=current_user.id, portfolio_id=portfolio_id)

    if not portfolio:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No portfolio with that id for this user "
                                                                   "in the database.")

    return PortfolioPublic(**portfolio.dict())


@router.delete("/{portfolio_id}", name="portfolio:delete-by-id", status_code=HTTP_200_OK, response_model=PortfolioPublic)
async def delete_portfolio_by_id(portfolio_id: int,
                               current_user: UserInDB = Depends(get_current_active_user),
                               portfolio_repo: PortfoliosRepository = Depends(get_repository(PortfoliosRepository)
                                                                              )) -> PortfolioPublic:
    portfolio = await portfolio_repo.delete_portfolio_by_id(user_id=current_user.id, portfolio_id=portfolio_id)

    if not portfolio:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No portfolio with that id for this user "
                                                                   "in the database.")

    return PortfolioPublic(**portfolio.dict())
