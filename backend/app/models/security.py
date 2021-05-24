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


class SecurityInDB(SecurityBase):
    """Instances of securities registered in database."""
    ticker: str
    type: str


class SecuritiesAddedToDB(CoreModel):
    """Contains list of SecurityInDB models that were added to DB."""
    message: str = "The following tickers have been successfully posted to the database:"
    securities: List[SecurityInDB]


class InvalidTickers(CoreModel):
    """List of invalid tickers that were not added to DB."""
    message: str = "The following tickers are invalid and have not been posted to the database:"
    tickers: List[str]


class SecuritiesAlreadyInDB(CoreModel):
    """Contains list of SecurityInDB models that were already added to DB and cannot be re-added."""
    message: str = "The following tickers were already included in the database and cannot be re-added:"
    securities: List[SecurityInDB]


class POSTTickerResponse(CoreModel):
    """Response model for POST ticker endpoint"""
    added_tickers: SecuritiesAddedToDB
    existing_tickers: SecuritiesAlreadyInDB
    invalid_tickers: InvalidTickers


class EquityCreate(SecurityBase):
    ticker: str
    name: str
    country: str
    sector: str
    industry: str
    exchange: str


class EquityUpdate(SecurityBase):
    pass


class EquityInDB(SecurityBase):
    ticker: str
    name: str
    country: str
    sector: str
    industry: str
    exchange: str


class EquityPublic(SecurityBase):
    pass


class ETFCreate(SecurityBase):
    ticker: str
    name: str
    exchange: str
    bond_position: float
    bond_maturity: float
    bond_duration: float
    bb_bonds: float
    aa_bonds: float
    aaa_bonds: float
    a_bonds: float
    other_bonds: float
    b_bonds: float
    bbb_bonds: float
    below_b_bonds: float
    us_gov_bonds: float
    stock_position: float
    real_estate: float
    consumer_cyclical: float
    basic_materials: float
    consumer_defensive: float
    technology: float
    communication_services: float
    financial_services: float
    utilities: float
    industrials: float
    energy: float
    healthcare: float


class ETFInDB(SecurityBase):
    ticker: str
    name: str
    exchange: str
