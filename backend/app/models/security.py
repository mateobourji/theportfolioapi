from typing import Optional, List, Type
from enum import Enum
from app.models.core import IDModelMixin, CoreModel


# class SecurityType(str, Enum):
#     equity = "equity"
#     fixed_income = "fixed_income"
#     etf = "etf"
#     cryptocurrency = "cryptocurrency"
#     index = "index"
#     commodity = "commodity"

class SecurityBase(CoreModel):
    """
    All common characteristics of our Ticker resource
    """


class SecurityCreate(SecurityBase):
    tickers: List[str]


class SecurityUpdate(SecurityBase):
    pass

class SecurityInDB(IDModelMixin, SecurityBase):
    ticker: str
    type: str

class SecurityPublic(IDModelMixin, SecurityBase):
    pass




class EquityCreate(SecurityBase):
    ticker: str
    name: str
    country: str
    summary: str
    sector: str
    industry: str
    exchange: str


class EquityUpdate(SecurityBase):
    pass


class EquityInDB(IDModelMixin, SecurityBase):
    ticker: str
    name: str
    country: str
    summary: str
    sector: str
    industry: str
    exchange: str


class EquityPublic(IDModelMixin, SecurityBase):
    pass
