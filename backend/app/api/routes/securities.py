from typing import List, Optional, Dict
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from app.models.security import SecurityInDB, SecuritiesAddedToDB, POSTTickerResponse
from app.models.equity import EquityCreate, EquityInDB
from app.models.etf import ETFCreate, ETFInDB, ETFQueryParams
import yfinance as yf
from app.db.repositories.securities import SecuritiesRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


# TODO: return tickers that were not valid and were not added to db, and tickers that are already in db
@router.post("/tickers/", name="instruments:add-tickers", response_model=POSTTickerResponse,
             status_code=HTTP_201_CREATED)
async def add_tickers(ticker_list: List[str] = Body(..., title="List of Tickers"),
                      tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                      ) -> POSTTickerResponse:
    tickers = await tickers_repo.add_tickers(tickers=ticker_list)

    return tickers


@router.get("/tickers/", name="instruments:get-tickers", response_model=List[SecurityInDB],
            status_code=HTTP_200_OK)
async def get_tickers(q: Optional[List[str]] = Query(None, title="List of tickers to filter."),
                      tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                      ) -> List[SecurityInDB]:
    securities = await tickers_repo.get_securities_by_ticker(tickers=q)

    if not securities:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="None of the securities are currently in the "
                                                                   "database. If they exist, please add then through"
                                                                   "the POST endpoint")

    return securities


@router.get("/equities/", name="equities:get-equities", response_model=List[EquityInDB],
            status_code=HTTP_200_OK)
async def get_equities(tickers: Optional[List[str]] = Query(None, title="List of equity tickers to filter."),
                       names: Optional[List[str]] = Query(None, title="List of company names to filter."),
                       sectors: Optional[List[str]] = Query(None, title="List of sectors to filter."),
                       industries: Optional[List[str]] = Query(None, title="List of industries to filter."),
                       countries: Optional[List[str]] = Query(None, title="List of countries to filter."),
                       exchanges: Optional[List[str]] = Query(None, title="List of stock exchanges to filter."),
                       tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                       ) -> List[EquityInDB]:
    equities = await tickers_repo.get_equities_by_ticker(tickers=tickers, names=names, sectors=sectors,
                                                         industries=industries, countries=countries,
                                                         exchanges=exchanges)

    if not equities:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No equities with the current filters in the "
                                                                   "database. If they exist, please add then through "
                                                                   "the POST endpoint")

    return equities


@router.get("/ETFs/", name="equities:get-ETFs", response_model=List[ETFInDB], status_code=HTTP_200_OK)
async def get_etfs(params: ETFQueryParams = Depends(),
                   tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                   ) -> List[ETFInDB]:
    etfs = await tickers_repo.get_etf(params=params)

    if not etfs:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No ETFs with the current filters in the "
                                                                   "database. If they exist, please add then through "
                                                                   "the POST endpoint")

    return etfs
