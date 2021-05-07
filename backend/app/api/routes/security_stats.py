from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from app.core.Download_Data import Download_Data
import datetime
from app.core.check_tickers import check_tickers
from app.core.Hist_Data import Hist_Data

router = APIRouter()

@router.get("/", name="data:download-stats", status_code=HTTP_200_OK)
async def return_hist_returns(q: List[str] = Query(..., title="List of securities", min_length=2),
                           start: Optional[datetime.date] = "2000-01-01",
                           end: Optional[datetime.date] = datetime.date.today()):
    check_tickers(q)
    data = Download_Data(q, 'YF', start=start, end=end)
    hist_data = Hist_Data(securities=q, prices=data.prices.fillna(0), dividends=data.dividends.fillna(0))
    return {'returns': hist_data.returns,
            'mean': hist_data.mean,
            'std': hist_data.std,
            'skew': hist_data.skew,
            'kurtosis': hist_data.kurtosis,
            'corr': hist_data.corr,
            'cov': hist_data.cov}
