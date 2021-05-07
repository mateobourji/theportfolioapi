from typing import List, Optional, Dict
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from app.core.Download_Data import Download_Data
import datetime
from app.core.check_tickers import check_tickers
from app.core.Hist_Data import Hist_Data
from app.models.security import SecurityCreate, SecurityInDB
from app.models.equity import EquityCreate
import yfinance as yf
from app.db.repositories.securities import SecuritiesRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.post("/", name="securities:add-tickers", status_code=HTTP_201_CREATED)
async def add_tickers(ticker_list: SecurityCreate = Body(..., title="List of symbols"),
                      tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))) -> Dict:
    added_tickers = {}
    invalid_tickers = []
    for ticker in ticker_list.dict()['tickers']:
        data = yf.Ticker(ticker).info
        equity = EquityCreate(ticker=ticker, name=data['shortName'], country=data['country'],
                              summary=data['longBusinessSummary'], sector=data['sector'], industry=data['industry'],
                              exchange=data['exchange'])
        added_tickers[ticker] = await tickers_repo.add_equity(new_equity=equity)
        print(added_tickers)
    # except:
    #     invalid_tickers.append(ticker)
    #     continue

    return added_tickers


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
