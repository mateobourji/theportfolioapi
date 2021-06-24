from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from app.models.equity import EquityQueryParams, EquityPublic
from app.models.etf import ETFQueryParams, ETFPublic
from app.db.repositories.assets import SecuritiesRepository
from app.api.dependencies.database import get_repository


router = APIRouter()


@router.get("/equities/", name="screener:get-equities", status_code=HTTP_200_OK,
            response_model=List[EquityPublic],
            response_description="Returns an array of equities that meet the filter criteria. If no filters are "
                                 "selected, returns all equities in the database.")
async def get_equities(params: EquityQueryParams = Depends(),
                       tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                       ) -> List[EquityPublic]:
    equities = await tickers_repo.get_equities_by_ticker(params=params)

    if not equities:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No equities with the current filters in the "
                                                                   "database. If they exist, please add then through "
                                                                   "the POST endpoint")

    return equities


@router.get("/ETFs/", name="screener:get-ETFs", status_code=HTTP_200_OK,
            response_model=List[ETFPublic],
            response_description="Returns an array of ETFs that meet the filter criteria. If no filters are "
                                 "selected, returns all ETFs in the database.")
async def get_etfs(params: ETFQueryParams = Depends(),
                   tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                   ) -> List[ETFPublic]:
    etfs = await tickers_repo.get_etf(params=params)

    if not etfs:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No ETFs with the current filters in the "
                                                                   "database. If they exist, please add then through "
                                                                   "the POST endpoint")

    return etfs
