from app.models.core import CoreModel
from typing import Optional, List
from fastapi import Query
from typing import TypeVar

PandasDataFrame = TypeVar('pandas.core.frame.DataFrame')

class HistoricalPerformanceBase(CoreModel):
    """
    All common characteristics of our ETF resource
    """

class HistoricalPerformancePublic(HistoricalPerformanceBase):
    securities: List[str]
    prices: PandasDataFrame
    dividends: PandasDataFrame
    returns: PandasDataFrame
    mean: PandasDataFrame
    std: PandasDataFrame
    corr: PandasDataFrame
    cov: PandasDataFrame