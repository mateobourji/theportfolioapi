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
                 tickers: Optional[List[str]] = Query(None, description="List of equity tickers to filter."),
                 names: Optional[List[str]] = Query(None, description="List of company names to filter."),
                 sectors: Optional[List[str]] = Query(None, description="List of sectors to filter."),
                 industries: Optional[List[str]] = Query(None, description="List of industries to filter."),
                 countries: Optional[List[str]] = Query(None, description="List of countries to filter."),
                 exchanges: Optional[List[str]] = Query(None, description="List of stock exchanges to filter.")):
        self.tickers = (lambda x: tuple(x) if x is not None else x)(tickers)
        self.names = (lambda x: tuple(x) if x is not None else x)(names)
        self.sectors = (lambda x: tuple(x) if x is not None else x)(sectors)
        self.industries = (lambda x: tuple(x) if x is not None else x)(industries)
        self.countries = (lambda x: tuple(x) if x is not None else x)(countries)
        self.exchanges = (lambda x: tuple(x) if x is not None else x)(exchanges)

class EquityPublic(EquityBase):
    ticker: str
    name: str
    country: str
    sector: str
    industry: str
    exchange: str