import pandas as pd


class Hist_Data:
    def __init__(self, securities, prices, dividends, corr_method='pearson'):
        self.securities = securities
        self._prices = prices
        self._dividends = dividends
        self._returns = self._calculate_returns()
        self._mean = self._calculate_mean()
        self._std = self._calculate_std()
        self._skew = self._calculate_skew()
        self._kurtosis = self._calculate_kurtosis()
        self._corr = self._calculate_corr(method=corr_method)
        self._cov = self._calculate_cov()
        # returns + summary statistics are set as attributes (not methods) as they will be called '000s of times
        # in monte carlo sim in Portfolio class

    @property
    def prices(self):
        return self._prices

    @property
    def dividends(self):
        return self._dividends

    @property
    def returns(self):
        return self._returns

    @property
    def mean(self):
        return self._mean

    @property
    def std(self):
        return self._std

    @property
    def skew(self):
        return self._skew

    @property
    def kurtosis(self):
        return self._kurtosis

    @property
    def corr(self):
        return self._corr

    @property
    def cov(self):
        return self._cov

    def _calculate_mean(self):
        return self.returns.mean()

    def _calculate_std(self):
        return self.returns.std()

    def _calculate_skew(self):
        return self.returns.skew()

    def _calculate_kurtosis(self):
        return self.returns.kurtosis()

    def _calculate_corr(self, method='pearson'):
        return self.returns.corr(method=method)

    def _calculate_cov(self):
        return self.returns.cov()

    def _calculate_returns(self):
        # TODO: option for dividend reinvestment
        # TODO: implement/option using log returns
        return (self._prices + self._dividends).div(self._prices.shift(1)).iloc[1:] - 1
