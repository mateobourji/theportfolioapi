from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from starlette.responses import StreamingResponse, FileResponse, HTMLResponse
from backend.app.core.historical_data import Hist_Data, Hist_Data_Plot
import datetime
from backend.app.core.check_tickers import check_tickers
from backend.app.models.historical_performance import HistoricalPerformancePublic
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, save
import codecs

router = APIRouter()


@router.get("/data/", name="historical-performance:data", status_code=HTTP_200_OK,
            response_model=HistoricalPerformancePublic)
async def historical_performance(q: List[str] = Query(..., title="List of securities"),
                                 start: Optional[datetime.date] = "2000-01-01",
                                 end: Optional[datetime.date] = datetime.date.today()) -> HistoricalPerformancePublic:
    check_tickers(q)
    hist_data = Hist_Data(securities=q, start=start, end=end)
    return HistoricalPerformancePublic.parse_obj(vars(hist_data))

@router.get("/graph/", name="historical-performance:graphs", status_code=HTTP_200_OK, response_class=HTMLResponse)
async def historical_performance(q: List[str] = Query(..., title="List of securities"),
                                 start: Optional[datetime.date] = "2000-01-01",
                                 end: Optional[datetime.date] = datetime.date.today()):
    check_tickers(q)

    hist_data_plot = Hist_Data_Plot(securities=q, start=start, end=end)

    return HTMLResponse(codecs.open(hist_data_plot.plot_summary()).read())

