from typing import List
from backend.app.models.core import CoreModel


class TickerBase(CoreModel):
    """
    All common characteristics of our Ticker resource
    """


class TickerInDB(TickerBase):
    """Instances of securities registered in database."""
    ticker: str
    type: str

class TickerPublic(TickerBase):
    """Instances of securities registered in database."""
    ticker: str
    type: str

class TickersAddedToDB(CoreModel):
    """Contains list of TickerInDB models that were added to DB."""
    message: str = "The following tickers have been successfully posted to the database:"
    securities: List[TickerInDB]


class InvalidTickers(CoreModel):
    """List of invalid tickers that were not added to DB."""
    message: str = "The following tickers are invalid and have not been posted to the database:"
    tickers: List[str]


class TickersAlreadyInDB(CoreModel):
    """Contains list of TickerInDB models that were already added to DB and cannot be re-added."""
    message: str = "The following tickers were already included in the database and cannot be re-added:"
    securities: List[TickerInDB]


class POSTTickerResponse(CoreModel):
    """Response model for POST ticker endpoint"""
    added_tickers: TickersAddedToDB
    existing_tickers: TickersAlreadyInDB
    invalid_tickers: InvalidTickers






