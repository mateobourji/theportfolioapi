import codecs
import datetime
from typing import List, Optional

from fastapi import APIRouter, Query, Depends
from starlette.responses import HTMLResponse
from starlette.status import HTTP_200_OK

from app.core.check_tickers import check_tickers
from app.core.historical_data import Hist_Data, Hist_Data_Plot
from app.models.historical_performance import HistoricalPerformancePublic
from app.api.dependencies.auth import get_current_active_user
from app.models.user import UserInDB

router = APIRouter()


@router.get("/statistics/data/", name="historical-performance:data", status_code=HTTP_200_OK,
            response_model=HistoricalPerformancePublic)
async def historical_performance(current_user: UserInDB = Depends(get_current_active_user),
                                 q: List[str] = Query(..., title="List of securities"),
                                 start: Optional[datetime.date] = "2000-01-01",
                                 end: Optional[datetime.date] = datetime.date.today()) -> HistoricalPerformancePublic:
    check_tickers(q)
    hist_data = Hist_Data(securities=q, start=start, end=end)
    return HistoricalPerformancePublic.parse_obj(vars(hist_data))

@router.get("/statistics/graph/", name="historical-performance:graphs", status_code=HTTP_200_OK, response_class=HTMLResponse)
async def historical_performance(current_user: UserInDB = Depends(get_current_active_user),
                                 q: List[str] = Query(..., title="List of securities"),
                                 start: Optional[datetime.date] = "2000-01-01",
                                 end: Optional[datetime.date] = datetime.date.today()):
    check_tickers(q)

    hist_data_plot = Hist_Data_Plot(securities=q, start=start, end=end)

    return HTMLResponse(codecs.open(hist_data_plot.plot_summary()).read())

