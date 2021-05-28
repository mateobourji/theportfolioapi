from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from app.models.equity import EquityInDB, EquityQueryParams
from app.models.etf import ETFInDB, ETFQueryParams
from app.db.repositories.assets import SecuritiesRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


# TODO: return tickers that were not valid and were not added to db, and tickers that are already in db


@router.get("/equities/", name="equities:get-equities", response_model=List[EquityInDB],
            status_code=HTTP_200_OK)
async def get_equities(params: EquityQueryParams = Depends(),
                       tickers_repo: SecuritiesRepository = Depends(get_repository(SecuritiesRepository))
                       ) -> List[EquityInDB]:
    equities = await tickers_repo.get_equities_by_ticker(params=params)

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