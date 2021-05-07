import datetime

from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from sample.Download_Data import Download_Data
from sample.Hist_Data import Hist_Data
from sample.Portfolio import Portfolio
import yfinance as yf

app = FastAPI()

# memoize valid security tickers to avoid expensive call to check yfinance API each time
valid_tickers = {}


def check_tickers(ticker_list):
    new_tickers = list(set(ticker_list).difference(set(valid_tickers.keys())))
    invalid_tickers = []
    ticker_info = yf.Tickers(new_tickers)

    for ticker in new_tickers:
        #yfinance still returns invalid tickers, but in which case the tickers info dictionary is size 1 (junk info)
        if len(ticker_info.tickers[ticker].info) == 1:
            invalid_tickers.append(ticker)
        else:
            valid_tickers[ticker] = {'sector': ticker_info.tickers[ticker].info['sector'],
                                     'country': ticker_info.tickers[ticker].info['country']}

    if not invalid_tickers:
        return 1
    else:
        error_msg = {"error": "The following tickers are not valid:", "invalid_tickers": invalid_tickers}
        raise HTTPException(status_code=404, detail=error_msg)


@app.get("/security-data/")
async def return_hist_data(q: List[str] = Query(..., title="List of securities", min_length=2),
                           start: Optional[datetime.date] = "2000-01-01",
                           end: Optional[datetime.date] = datetime.date.today()):
    check_tickers(q)
    data = Download_Data(q, 'YF', start=start, end=end)
    return {'prices': data.prices.fillna(0).to_dict(), 'dividends': data.dividends.fillna(0).to_dict()}


@app.get("/security-stats/")
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


@app.get("/optimized-portfolio/")
async def return_opt_portfolio(q: List[str] = Query(..., title="List of securities", min_length=2),
                           start: Optional[datetime.date] = "2000-01-01",
                           end: Optional[datetime.date] = datetime.date.today()):
    check_tickers(q)
    data = Download_Data(q, 'YF', start=start, end=end)
    hist_data = Hist_Data(securities=q, prices=data.prices, dividends=data.dividends)
    portfolio = Portfolio(hist_data)
    return portfolio.optimal_portfolio()

