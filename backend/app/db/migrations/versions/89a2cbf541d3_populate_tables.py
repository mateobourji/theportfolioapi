"""populate_tables
Revision ID: 89a2cbf541d3
Revises: 12345678654
Create Date: 2021-06-28 11:25:05.168534
"""
from alembic import op
import sqlalchemy as sa
from app.models.equity import EquityCreate
import json
import os

# revision identifiers, used by Alembic
from app.models.etf import ETFCreate
from app.models.fund import FundCreate

revision = '89a2cbf541d3'
down_revision = '12345678654'
branch_labels = None
depends_on = None


def populate_equities_table():
    directory = os.fsencode('app/db/migrations/data/Equities')

    for file in os.listdir(directory):
        with open('app/db/migrations/data/Equities/' + file.decode("utf-8")) as json_file:
            data = json.load(json_file)
            equities = []
            for asset in data.keys():
                try:
                    data[asset]['ticker'] = asset
                    equities.append(EquityCreate.parse_obj(data[asset]).dict())
                except:
                    continue
            op.get_bind().execute(sa.sql.text("""
                                                INSERT INTO equities (ticker, short_name, long_name, currency, sector,
                                                industry, exchange, market, country, city, summary)
                                                VALUES (:ticker, :short_name, :long_name, :currency, :sector, :industry, 
                                                :exchange, :market, :country, :city, :summary);
                                               """),
                                  equities)


def populate_etfs_table():
    directory = os.fsencode('app/db/migrations/data/ETFs')

    for file in os.listdir(directory):
        with open('app/db/migrations/data/ETFs/' + file.decode("utf-8")) as json_file:
            data = json.load(json_file)
            etfs = []
            for asset in data.keys():
                try:
                    data[asset]['ticker'] = asset
                    etfs.append(ETFCreate.parse_obj(data[asset]).dict())
                except:
                    continue
            op.get_bind().execute(sa.sql.text("""
                                                INSERT INTO etfs (ticker, short_name, long_name, summary, currency,
                                                category, family, exchange, market)
                                                VALUES (:ticker, :short_name, :long_name, :summary, :currency, 
                                                :category, :family, :exchange, :market);
                                               """),
                                  etfs)


def populate_funds_table():
    directory = os.fsencode('app/db/migrations/data/Funds')

    for file in os.listdir(directory):
        with open('app/db/migrations/data/Funds/' + file.decode("utf-8")) as json_file:
            print(file)
            data = json.load(json_file)
            funds = []
            for asset in data.keys():
                try:
                    data[asset]['ticker'] = asset
                    funds.append(FundCreate.parse_obj(data[asset]).dict())
                except:
                    continue

            op.get_bind().execute(sa.sql.text("""
                                                INSERT INTO funds (ticker, short_name, long_name, summary, currency,
                                                category, family, exchange, market)
                                                VALUES (:ticker, :short_name, :long_name, :summary, :currency, 
                                                :category, :family, :exchange, :market);
                                               """),
                                  funds)


def depopulate_equities_table():
    op.get_bind().execute(sa.sql.text("""
                                        TRUNCATE table equities;
                                       """))


def depopulate_etfs_table():
    op.get_bind().execute(sa.sql.text("""
                                        TRUNCATE table etfs;
                                       """))


def depopulate_funds_table():
    op.get_bind().execute(sa.sql.text("""
                                        TRUNCATE table funds;
                                       """))


def upgrade() -> None:
    populate_equities_table()
    populate_etfs_table()
    populate_funds_table()


def downgrade() -> None:
    depopulate_equities_table()
    depopulate_etfs_table()
    depopulate_funds_table()
