from app.models.core import CoreModel
from typing import Optional, List
from fastapi import Query
from pydantic import Field


class ETFBase(CoreModel):
    """
    All common characteristics of our ETF resource
    """


class ETFCreate(ETFBase):
    ticker: str
    name: str
    exchange: str
    bond_position: float
    investment_grade_bonds: float
    junk_bonds: float
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


class ETFBondData(CoreModel):
    bond_position: float
    bb_bonds: float
    aa_bonds: float
    aaa_bonds: float
    a_bonds: float
    other_bonds: float
    b_bonds: float
    bbb_bonds: float
    below_b_bonds: float
    us_gov_bonds: float


class ETFInDB(ETFBase):
    ticker: str
    name: str
    exchange: str
    bond_position: float
    investment_grade_bonds: float
    junk_bonds: float
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


class ETFQueryParams:
    def __init__(self,
                 tickers: Optional[List[str]] = Query(None, title="List of equity tickers to filter."),
                 names: Optional[List[str]] = Query(None, title="List of company names to filter."),
                 exchanges: Optional[List[str]] = Query(None, title="List of stock exchanges to filter."),
                 min_stock: Optional[float] = Query(None, le=1, description="Minimum % of equity holdings."),
                 min_bond: Optional[float] = Query(None, le=1, description="Minimum % of fixed income holdings."),
                 min_investment_grade: Optional[float] = Query(None, le=1,
                                                               description="Minimum % of investment grade within "
                                                                           "fixed-income holdings."),
                 max_investment_grade: Optional[float] = Query(None, le=1,
                                                               description="Maximum % of investment grade within "
                                                                           "fixed-income holdings."),
                 min_junk_bonds: Optional[float] = Query(None, le=1,
                                                         description="Minimum % of junk bonds within fixed-income "
                                                                     "holdings."),
                 max_junk_bonds: Optional[float] = Query(None, le=1,
                                                         description="Maximum % of junk bonds within fixed-income "
                                                                     "holdings."),
                 min_real_estate: Optional[float] = Query(None, le=1,
                                                          description="Minimum % of real estate sector exposure "
                                                                      "within equity holdings"),
                 max_real_estate: Optional[float] = Query(None, le=1,
                                                          description="Maximum % of real estate sector exposure "
                                                                      "within equity holdings"),
                 min_consumer_cyclical: Optional[float] = Query(None, le=1,
                                                                description="Minimum % of consumer cyclical sector "
                                                                            "exposure within equity holdings"),
                 max_consumer_cyclical: Optional[float] = Query(None, le=1,
                                                                description="Maximum % of consumer cyclical sector "
                                                                            "exposure within equity holdings"),
                 min_basic_materials: Optional[float] = Query(None, le=1,
                                                              description="Minimum % of basic materials sector "
                                                                          "exposure within equity holdings"),
                 max_basic_materials: Optional[float] = Query(None, le=1,
                                                              description="Maximum % of basic materials sector "
                                                                          "exposure within equity holdings"),
                 min_consumer_defensive: Optional[float] = Query(None, le=1,
                                                                 description="Minimum % of consumer defensive sector "
                                                                             "exposure within equity holdings"),
                 max_consumer_defensive: Optional[float] = Query(None, le=1,
                                                                 description="Maximum % of consumer defensive sector "
                                                                             "exposure within equity holdings"),
                 min_technology: Optional[float] = Query(None, le=1,
                                                         description="Minimum % of technology sector exposure within "
                                                                     "equity holdings"),
                 max_technology: Optional[float] = Query(None, le=1,
                                                         description="Maximum % of technology sector exposure within "
                                                                     "equity holdings"),
                 min_communication_services: Optional[float] = Query(None, le=1,
                                                                     description="Minimum % of communication services "
                                                                                 "sector exposure within equity "
                                                                                 "holdings"),
                 max_communication_services: Optional[float] = Query(None, le=1,
                                                                     description="Maximum % of communication services "
                                                                                 "sector exposure within equity "
                                                                                 "holdings"),
                 min_financial_services: Optional[float] = Query(None, le=1,
                                                                 description="Minimum % of financial services sector "
                                                                             "exposure within equity holdings"),
                 max_financial_services: Optional[float] = Query(None, le=1,
                                                                 description="Maximum % of financial services sector "
                                                                             "exposure within equity holdings"),
                 min_utilities: Optional[float] = Query(None, le=1,
                                                        description="Minimum % of utilities sector exposure within "
                                                                    "equity holdings"),
                 max_utilities: Optional[float] = Query(None, le=1,
                                                        description="Maximum % of utilities sector exposure within "
                                                                    "equity holdings"),
                 min_industrials: Optional[float] = Query(None, le=1,
                                                          description="Minimum % of industrials sector exposure "
                                                                      "within equity holdings"),
                 max_industrials: Optional[float] = Query(None, le=1,
                                                          description="Maximum % of industrials sector exposure "
                                                                      "within equity holdings"),
                 min_energy: Optional[float] = Query(None, le=1,
                                                     description="Minimum % of energy sector exposure within equity "
                                                                 "holdings"),
                 max_energy: Optional[float] = Query(None, le=1,
                                                     description="Maximum % of energy sector exposure within equity "
                                                                 "holdings"),
                 min_healthcare: Optional[float] = Query(None, le=1,
                                                         description="Minimum % of healthcare sector exposure within "
                                                                     "equity holdings"),
                 max_healthcare: Optional[float] = Query(None, le=1,
                                                         description="Maximum % of healthcare sector exposure within "
                                                                     "equity holdings"),
                 ):
        self.tickers = (lambda x: tuple(x) if x is not None else x)(tickers)
        self.names = (lambda x: tuple(x) if x is not None else x)(names)
        self.exchanges = (lambda x: tuple(x) if x is not None else x)(exchanges)
        self.min_stock = min_stock
        self.min_bond = min_bond
        self.min_investment_grade = min_investment_grade
        self.max_investment_grade = max_investment_grade
        self.min_junk_bonds = min_junk_bonds
        self.max_junk_bonds = max_junk_bonds
        self.min_real_estate = min_real_estate
        self.max_real_estate = max_real_estate
        self.min_consumer_cyclical = min_consumer_cyclical
        self.max_consumer_cyclical = max_consumer_cyclical
        self.min_basic_materials = min_basic_materials
        self.max_basic_materials = max_basic_materials
        self.min_consumer_defensive = min_consumer_defensive
        self.max_consumer_defensive = max_consumer_defensive
        self.min_technology = min_technology
        self.max_technology = max_technology
        self.min_communication_services = min_communication_services
        self.max_communication_services = max_communication_services
        self.min_financial_services = min_financial_services
        self.max_financial_services = max_financial_services
        self.min_utilities = min_utilities
        self.max_utilities = max_utilities
        self.min_industrials = min_industrials
        self.max_industrials = max_industrials
        self.min_energy = min_energy
        self.max_energy = max_energy
        self.min_healthcare = min_healthcare
        self.max_healthcare = max_healthcare
