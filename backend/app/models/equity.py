from app.models.core import CoreModel


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


class EquityPublic(EquityBase):
    pass
