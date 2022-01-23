from fastapi import HTTPException
import yfinance as yf
import logging

# memoize valid security tickers to avoid expensive call to check yfinance API each time
valid_tickers = {}

db_logger = logging.getLogger("DB")


def check_tickers(ticker_list):
    new_tickers = list(set(ticker_list).difference(set(valid_tickers.keys())))
    invalid_tickers = []
    ticker_info = yf.Tickers(new_tickers)

    for ticker in new_tickers:
        # yfinance still returns invalid tickers, but in which case the tickers info dictionary is size 1 (junk info)
        if len(ticker_info.tickers[ticker].info) == 1:
            db_logger.log(level=logging.INFO,
                          msg="%s not found on Yahoo Finance. Adding it to invalid tickers.")
            invalid_tickers.append(ticker)
        else:
            valid_tickers[ticker] = {'sector': ticker_info.tickers[ticker].info['sector'],
                                     'country': ticker_info.tickers[ticker].info['country']}

    if not invalid_tickers:
        return 1
    else:
        error_msg = {"error": "The following tickers are not valid:", "invalid_tickers": invalid_tickers}
        raise HTTPException(status_code=404, detail=error_msg)
