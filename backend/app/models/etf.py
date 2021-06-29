from app.models.core import CoreModel
from typing import Optional, List
from fastapi import Query
from pydantic import validator


class ETFBase(CoreModel):
    """
    All common characteristics of our ETF resource
    """

def na_if_none(input) -> str:
    if isinstance(input, str):
        return input
    else:
        return "n/a"

class ETFCreate(ETFBase):
    ticker: str
    short_name: str
    long_name: str
    summary: Optional[str]
    currency: Optional[str]
    category: Optional[str]
    family: Optional[str]
    exchange: Optional[str]
    market: Optional[str]

    #validators
    _na_if_none_summary = validator('summary', allow_reuse=True)(na_if_none)
    _na_if_none_currency = validator('currency', allow_reuse=True)(na_if_none)
    _na_if_none_category = validator('category', allow_reuse=True)(na_if_none)
    _na_if_none_family = validator('family', allow_reuse=True)(na_if_none)
    _na_if_none_exchange = validator('exchange', allow_reuse=True)(na_if_none)
    _na_if_none_market = validator('market', allow_reuse=True)(na_if_none)

class ETFInDB(ETFBase):
    ticker: str
    short_name: str
    long_name: str
    summary: str
    currency: str
    category: str
    family: str
    exchange: str
    market: str

class ETFPublic(ETFBase):
    ticker: str
    short_name: str
    long_name: str
    summary: str
    currency: str
    category: str
    family: str
    exchange: str
    market: str

class ETFQueryParams:
    def __init__(self,
                 ticker: Optional[List[str]] = Query(None, description="example: ADRE"),
                 long_name: Optional[List[str]] = Query(None, description="example: SPDR Bloomberg Barclays Emerging Markets Local Bond ETF"),
                 currency: Optional[List[str]] = Query(None, description="example: USD"),
                 category: Optional[List[str]] = Query(None, description="example: Industrials, Emerging Markets Bond"),
                 family: Optional[List[str]] = Query(None, description="example: iShares"),
                 exchange: Optional[List[str]] = Query(None, description="example: NMS"),
                 market: Optional[List[str]] = Query(None, description="example: us_market")
                 ):
        # Optional WHERE IN ANY() SQL query in repo requires tuple of values to filter or NULL/None to ignore filter
        # Lambda function below returns tuple if list is passed, otherwise None
        self.ticker = (lambda x: tuple(x) if x is not None else x)(ticker)
        self.long_name = (lambda x: tuple(x) if x is not None else x)(long_name)
        self.currency = (lambda x: tuple(x) if x is not None else x)(currency)
        self.category = (lambda x: tuple(x) if x is not None else x)(category)
        self.family = (lambda x: tuple(x) if x is not None else x)(family)
        self.exchange = (lambda x: tuple(x) if x is not None else x)(exchange)
        self.market = (lambda x: tuple(x) if x is not None else x)(market)
