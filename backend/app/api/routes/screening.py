from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app.db.repositories.etf import ETFRepository
from app.models.equity import EquityQueryParams, EquityPublic
from app.models.etf import ETFQueryParams, ETFPublic
from app.db.repositories.equity import EquityRepository
from app.api.dependencies.database import get_repository


router = APIRouter()


@router.get("/equities/", name="screener:get-equities", status_code=HTTP_200_OK,
            response_model=List[EquityPublic],
            response_description="Returns an array of equities that meet the filter criteria. If no filters are "
                                 "selected, returns all equities in the database.")
async def get_equities(params: EquityQueryParams = Depends(),
                       equities_repo: EquityRepository = Depends(get_repository(EquityRepository))
                       ) -> List[EquityPublic]:
    equities = await equities_repo.get_equities(params=params)

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
                   etfs_repo: ETFRepository = Depends(get_repository(ETFRepository))
                   ) -> List[ETFPublic]:
    etfs = await etfs_repo.get_etf(params=params)

    if not etfs:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No ETFs with the current filters in the "
                                                                   "database. If they exist, please add then through "
                                                                   "the POST endpoint")

    return etfs
