from typing import List
from app.models.core import CoreModel


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






