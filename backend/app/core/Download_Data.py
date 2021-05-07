import pandas as pd
import yfinance as yf
import datetime

class Download_Data:

    def __init__(self, securities, provider, start="2000-01-01", end=datetime.date.today()):
        self.securities = securities
        self._provider = provider
        self._start = start
        self._end = end
        self._data = self._download_data()
        self._dividends = self._get_dividends()
        self._prices = self._get_prices()


    @property
    def dividends(self):
        return self._dividends

    @property
    def prices(self):
        return self._prices

    def _download_data(self):
        # download all price and dividend data once, then split into two dataframes (one for prices, the other for
        # dividends)
        data = yf.download(self.securities, start=self._start, end=self._end, interval="1d", actions=True)

        return data

    def _get_dividends(self):
        dividends = self._data.drop(columns=["Close", "Adj Close", "Open", "High", "Low", "Volume", "Stock Splits"]) \
                        .droplevel(0, axis=1)

        return dividends

    def _get_prices(self):

        prices = self._data.drop(columns=["Adj Close", "Open", "High", "Low", "Volume", "Stock Splits", "Dividends"]) \
                     .droplevel(0, axis=1)

        return prices
