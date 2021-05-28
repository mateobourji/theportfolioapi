from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from app.models.ticker import TickerPublic
from app.db.repositories.assets import SecuritiesRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.post("/tickers/", name="instruments:add-tickers", response_model=List[TickerPublic],
             status_code=HTTP_201_CREATED)
async def add_tickers(ticker_list: List[str] = Body(..., title="List of Tickers"),
                      tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                      ) -> List[TickerPublic]:
    tickers = await tickers_repo.add_tickers(tickers=ticker_list)

    if not tickers:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Error: could not add tickers to database. They "
                                                                   "either already exist in the database, are not valid"
                                                                   "tickers, or not an asset class that is supported "
                                                                   "by the database")
    else:
        return tickers


@router.get("/tickers/", name="instruments:get-tickers", response_model=List[TickerPublic],
            status_code=HTTP_200_OK)
async def get_tickers(q: Optional[List[str]] = Query(None, title="List of tickers to filter."),
                      tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                      ) -> List[TickerPublic]:
    securities = await tickers_repo.get_securities_by_ticker(tickers=q)

    if not securities:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="None of the securities are currently in the "
                                                                   "database. If they exist, please add then through"
                                                                   "the POST endpoint")
    return securities
