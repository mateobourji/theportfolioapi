from typing import List, Optional, Dict
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from app.models.security import SecurityInDB, SecuritiesAddedToDB, POSTTickerResponse
from app.models.equity import EquityCreate
import yfinance as yf
from app.db.repositories.securities import SecuritiesRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


# TODO: return tickers that were not valid and were not added to db, and tickers that are already in db
@router.post("/", name="securities:add-tickers", response_model=POSTTickerResponse, status_code=HTTP_201_CREATED)
async def add_tickers(ticker_list: List[str] = Body(..., title="List of Tickers", max_length=4),
                      tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                      ) -> POSTTickerResponse:

    tickers = await tickers_repo.add_tickers(new_tickers=ticker_list)

    return tickers


@router.get("/", name="securities:get-securities-by-ticker", response_model=List[SecurityInDB], status_code=HTTP_200_OK)
async def get_securities_by_ticker(q: List[str] = Query(..., title="List of securities"),
                                   tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                                   ) -> List[SecurityInDB]:
    securities = await tickers_repo.get_securities_by_ticker(tickers=q)

    if not securities:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="One of the securities is not currently in the "
                                                                   "database. If it exists, please add it through the "
                                                                   "POST endpoint")

    return securities


@router.get("/all", name="securities:get-all-securities", response_model=List[SecurityInDB], status_code=HTTP_200_OK)
async def get_all_securities(tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                             ) -> List[SecurityInDB]:
    securities = await tickers_repo.get_all_securities()

    if not securities:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="There are currently no securities in the database.")

    return securities

