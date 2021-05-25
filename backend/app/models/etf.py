from app.models.core import CoreModel


class ETFBase(CoreModel):
    """
    All common characteristics of our ETF resource
    """


class ETFCreate(ETFBase):
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


class ETFInDB(ETFBase):
    ticker: str
    name: str
    exchange: str
