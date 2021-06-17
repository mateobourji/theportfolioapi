from app.models.core import CoreModel
from typing import Optional, List
from fastapi import Query


class EquityBase(CoreModel):
    """
    All common characteristics of our ETF resource
    """


class EquityCreate(EquityBase):
    ticker: str
    name: str
    country: str
    sector: str
    industry: str
    exchange: str


class EquityUpdate(EquityBase):
    pass


class EquityInDB(EquityBase):
    ticker: str
    name: str
    country: str
    sector: str
    industry: str
    exchange: str


class EquityQueryParams:
    def __init__(self,
                 tickers: Optional[List[str]] = Query(None, description="Filter equities by company ticker *(example: "
                                                                        "[\"AMZN\", \"AAPL\", \"TSLA\"] )*."),
                 names: Optional[List[str]] = Query(None, description="Filter equities by company name *(example: "
                                                                      "[\"Amazon.com, Inc.\", \"Apple Inc.\", "
                                                                      "\"Tesla, Inc.\"] )*."),
                 sectors: Optional[List[str]] = Query(None, description="Filter equities by sector *(example: "
                                                                        "[\"Consumer Cyclical\", \"Technology\"] )*."),
                 industries: Optional[List[str]] = Query(None, description="Filter equities by industry *(example: "
                                                                           "[\"Internet Retail\", \"Consumer "
                                                                           "Electronics\", \"Auto Manufacturers\"] )*."),
                 countries: Optional[List[str]] = Query(None,
                                                        description="Filter equities by country *(example: "
                                                                    "[\"United States\"] )*."),
                 exchanges: Optional[List[str]] = Query(None,
                                                        description="Filter equities by exchange listed on *(example: "
                                                                    "[\"NMS\"] )*.")):
        self.tickers = (lambda x: tuple(x) if x is not None else x)(tickers)
        self.names = (lambda x: tuple(x) if x is not None else x)(names)
        self.sectors = (lambda x: tuple(x) if x is not None else x)(sectors)
        self.industries = (lambda x: tuple(x) if x is not None else x)(industries)
        self.countries = (lambda x: tuple(x) if x is not None else x)(countries)
        self.exchanges = (lambda x: tuple(x) if x is not None else x)(exchanges)


class EquityPublic(EquityBase):
    """
    Returned equity with summary information.
    """
    ticker: str
    name: str
    country: str
    sector: str
    industry: str
    exchange: str
