from app.models.security import SecurityBase
from typing import Optional
from app.models.core import IDModelMixin, CoreModel


class EquityBase(SecurityBase):
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
    security_name: Optional[str]
    description: Optional[str]
    country: Optional[str]
    security_type: Optional[str]


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
