import pandas as pd
import yfinance as yf
import yahooquery as yq
import logging

core_logger = logging.getLogger("CORE")


class FinancialData:
    """class to download and structure financial data (stock prices, dividends) of securities"""

    def __init__(self, securities, provider, start, end):
        self.securities = securities
        self._provider = provider
        self._start = start
        self._end = end
        self._data = self._download_data()
        self.dividends = self._get_dividends()
        self.prices = self._get_prices()

    def _download_data(self):
        # download all price and dividend data once, then split into two dataframes (one for prices, the other for
        # dividends)
        data = yf.download(self.securities, start=self._start, end=self._end, interval="1d", actions=True)

        core_logger.log(level=logging.INFO,
                        msg="Downloading historical data from %s to %s every 1d for the following securities: %s"
                            % (self._start, self._end, self.securities))

        return data

    def _get_dividends(self):
        dividends = self._data.drop(columns=["Close", "Adj Close", "Open", "High", "Low", "Volume", "Stock Splits"])

        if len(self.securities) > 1:
            dividends = dividends.droplevel(0, axis=1)

        else:
            dividends.rename(columns={"Dividends": self.securities[0]}, inplace=True)
        # if there are no dividends, column type is numpy.int64, which cannot be encoded by FastAPI
        # therefore explicitly cast as float64

        return dividends.astype('float64')

    def _get_prices(self):
        prices = self._data.drop(columns=["Adj Close", "Open", "High", "Low", "Volume", "Stock Splits", "Dividends"])

        if len(self.securities) > 1:
            prices = prices.droplevel(0, axis=1)

        else:
            prices.rename(columns={"Close": self.securities[0]}, inplace=True)
        return prices


# noinspection PyBroadException
class TickerData:

    def __init__(self, ticker):
        self.ticker = ticker
        self._data = self._download_data()
        self.quoteType = self._get_quote_type()
        self.name = self._get_name()
        self.country = self._get_country()
        self.sector = self._get_sector()
        self.industry = self._get_industry()
        self.exchange = self._get_exchange()
        self.bond_position = self._get_bond_position()
        self.investment_grade_bonds = self._get_investment_grade_bonds()
        self.junk_bonds = self._get_junk_bonds()
        self.stock_position = self._get_stock_position()
        self.real_estate = self._get_real_estate_position()
        self.consumer_cyclical = self._get_consumer_cyclical_position()
        self.basic_materials = self._get_basic_materials_position()
        self.consumer_defensive = self._get_consumer_defensive_position()
        self.technology = self._get_technology_position()
        self.communication_services = self._get_communication_services_position()
        self.financial_services = self._get_financial_services_position()
        self.utilities = self._get_utilities_position()
        self.industrials = self._get_industrials_position()
        self.energy = self._get_energy_position()
        self.healthcare = self._get_healthcare_position()

    def _download_data(self):
        core_logger.log(level=logging.INFO,
                        msg="Downloading qualitative data for the following securities: %s"
                            % self.ticker)
        return yq.Ticker(self.ticker)

    def _get_quote_type(self):
        try:
            return self._data.quote_type[self.ticker.upper()]['quoteType']
        except:
            return None

    def _get_name(self):
        try:
            return self._data.quote_type[self.ticker.upper()]['shortName']
        except:
            return None

    def _get_country(self):
        try:
            return self._data.summary_profile[self.ticker.upper()]['country']
        except:
            return None

    def _get_sector(self):
        try:
            return self._data.summary_profile[self.ticker.upper()]['sector']
        except:
            return None

    def _get_industry(self):
        try:
            return self._data.summary_profile[self.ticker.upper()]['industry']
        except:
            return None

    def _get_exchange(self):
        try:
            return self._data.quote_type[self.ticker.upper()]['exchange']
        except:
            return None

    def _get_bond_position(self):
        try:
            return 1 - self._data.fund_category_holdings.iloc[0, 1]
        except:
            return None

    def _get_investment_grade_bonds(self):
        try:
            return self._data.fund_bond_ratings.iloc[0, 0] \
                   + self._data.fund_bond_ratings.iloc[1, 0] \
                   + self._data.fund_bond_ratings.iloc[2, 0] \
                   + self._data.fund_bond_ratings.iloc[3, 0] \
                   + self._data.fund_bond_ratings.iloc[6, 0]
        except:
            return None

    def _get_junk_bonds(self):
        try:
            return self._data.fund_bond_ratings.iloc[4, 0] \
                   + self._data.fund_bond_ratings.iloc[5, 0] \
                   + self._data.fund_bond_ratings.iloc[7, 0] \
                   + self._data.fund_bond_ratings.iloc[8, 0]
        except:
            return None

    def _get_stock_position(self):
        try:
            return self._data.fund_category_holdings.iloc[0, 1]
        except:
            return None

    def _get_real_estate_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[0, 0]
        except:
            return None

    def _get_consumer_cyclical_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[1, 0]
        except:
            return None

    def _get_basic_materials_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[2, 0]
        except:
            return None

    def _get_consumer_defensive_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[3, 0]
        except:
            return None

    def _get_technology_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[4, 0]
        except:
            return None

    def _get_communication_services_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[5, 0]
        except:
            return None

    def _get_financial_services_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[6, 0]
        except:
            return None

    def _get_utilities_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[7, 0]
        except:
            return None

    def _get_industrials_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[8, 0]
        except:
            return None

    def _get_energy_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[9, 0]
        except:
            return None

    def _get_healthcare_position(self):
        try:
            return self._data.fund_sector_weightings.iloc[10, 0]
        except:
            return None
