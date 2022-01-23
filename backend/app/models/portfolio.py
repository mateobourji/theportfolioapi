from datetime import datetime, date
from typing import List, Optional, Any

from pydantic.datetime_parse import parse_date

from app.models.core import CoreModel


def validate_date(v: Any) -> date:
    # if get_numeric(v, int) is not None:
    #     raise ValueError("Don't allow numbers")
    return parse_date(v)


class StrictDate(date):
    @classmethod
    def __get_validators__(cls):
        yield validate_date


class PortfolioBase(CoreModel):
    """
    All common characteristics of our Portfolio resource
    """


class PortfolioCreate(PortfolioBase):
    user_id: int
    portfolio_weights: str
    returns: float
    std: float
    sharpe_ratio: float
    return_over_risk: float
    optimization_type: str
    optimization_method: str


class PortfolioInDB(PortfolioBase):
    """Instances of securities registered in database."""
    id: int
    user_id: int
    portfolio_weights: str
    returns: float
    std: float
    sharpe_ratio: float
    return_over_risk: float
    added_at: datetime
    updated_at: datetime


class PortfolioPublic(CoreModel):
    """Instances of securities registered in database."""
    id: int
    user_id: int
    portfolio_weights: str
    returns: float
    std: float
    sharpe_ratio: float
    return_over_risk: float
    added_at: datetime
    updated_at: datetime


class PortfolioPOSTBodyParams(CoreModel):
    securities: List[str]
    start: Optional[StrictDate] = "2000-01-01"
    end: Optional[StrictDate] = datetime.today().date()

    # @validator("start", pre=True)
    # def parse_start(cls, value):
    #     return datetime.strptime(
    #         value,
    #         "%Y/%m/%d"
    #     ).date()
    #
    # @validator("end", pre=True)
    # def parse_end(cls, value):
    #     return datetime.strptime(
    #         value,
    #         "%Y/%m/%d"
    #     ).date()
    # TODO: end is today's dated

# Usage:
