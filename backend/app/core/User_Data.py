import pandas as pd
import numpy as np

class User_Data:

    def __init__(self, prices_file, dividends_file):
        self._securities = self._get_headers(prices_file)
        self._prices = self._get_records(prices_file)
        self._dividends = self._get_records(dividends_file)

    @property
    def securities(self):
        return self._securities

    @property
    def prices(self):
        return self._prices

    @property
    def dividends(self):
        return self._dividends

    @prices.setter
    def prices(self, file):
        prices = self._get_records(file)
        if prices.shape[0] == 0:
            raise Exception("Prices file contains no rows.")

    @dividends.setter
    def dividends(self, file):
        dividends = self._get_records(file)
        if dividends.columns != self.securities:
            raise Exception("Dividends and Prices securities do not match.")

    @classmethod
    def _get_headers(cls, prices_file):
        return list(pd.read_csv(prices_file).columns[1:])

    @classmethod
    def _get_records(cls, file):
        df = pd.read_csv(file)
        df[df.columns[0]] = df[df.columns[0]].astype(np.datetime64)
        df[df.columns[1:]] = df[df.columns[1:]].astype(float)
        df.set_index('Date', inplace=True)
        return df
