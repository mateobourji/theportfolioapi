from app.models.core import CoreModel
from typing import Optional, List
from fastapi import Query


class EquityBase(CoreModel):
    """
    All common characteristics of our ETF resource
    """


class EquityCreate(EquityBase):
    ticker: str
    short_name: str
    long_name: str
    summary: str
    currency: str
    sector: str
    industry: str
    exchange: str
    market: str
    country: str
    city: str


class EquityUpdate(EquityBase):
    pass


class EquityInDB(EquityBase):
    ticker: str
    short_name: str
    long_name: str
    summary: str
    currency: str
    sector: str
    industry: str
    exchange: str
    market: str
    country: str
    city: str


class EquityQueryParams:
    def __init__(self,
                 ticker: Optional[List[str]] = Query(None, description="Filter equities by company ticker *(example: "
                                                                        "[\"AMZN\", \"AAPL\", \"TSLA\"] )*."),
                 long_name: Optional[List[str]] = Query(None, description="Filter equities by company name *(example: "
                                                                           "[\"Amazon.com, Inc.\", \"Apple Inc.\", "
                                                                           "\"Tesla, Inc.\"] )*."),
                 sector: Optional[List[str]] = Query(None, description="Filter equities by sector *(example: "
                                                                        "[\"Consumer Cyclical\", \"Technology\"] )*."),
                 industry: Optional[List[str]] = Query(None, description="Filter equities by industry *(example: "
                                                                           "[\"Internet Retail\", \"Consumer "
                                                                           "Electronics\", \"Auto Manufacturers\"] )*."),
                 country: Optional[List[str]] = Query(None,
                                                        description="Filter equities by country *(example: "
                                                                    "[\"United States\"] )*."),
                 city: Optional[List[str]] = Query(None,
                                                     description="Filter equities by cities *(example: "
                                                                 "[\"San Francisco\"] )*."),
                 exchange: Optional[List[str]] = Query(None,
                                                        description="Filter equities by exchange listed on *(example: "
                                                                    "[\"NMS\"] )*."),
                 market: Optional[List[str]] = Query(None,
                                                      description="Filter equities by market *(example: "
                                                                  "[\"United States\"] )*."),
                 currency: Optional[List[str]] = Query(None,
                                                         description="Filter equities by currency *(example: "
                                                                           "[\"USD\"] )*.")):
        self.ticker = (lambda x: tuple(x) if x is not None else x)(ticker)
        self.long_name = (lambda x: tuple(x) if x is not None else x)(long_name)
        self.sector = (lambda x: tuple(x) if x is not None else x)(sector)
        self.industry = (lambda x: tuple(x) if x is not None else x)(industry)
        self.country = (lambda x: tuple(x) if x is not None else x)(country)
        self.city = (lambda x: tuple(x) if x is not None else x)(city)
        self.exchange = (lambda x: tuple(x) if x is not None else x)(exchange)
        self.market = (lambda x: tuple(x) if x is not None else x)(market)
        self.currency = (lambda x: tuple(x) if x is not None else x)(currency)


class EquityPublic(EquityBase):
    """
    Returned equity with summary information.
    """
    ticker: str
    short_name: str
    long_name: str
    summary: str
    currency: str
    sector: str
    industry: str
    exchange: str
    market: str
    country: str
    city: str
