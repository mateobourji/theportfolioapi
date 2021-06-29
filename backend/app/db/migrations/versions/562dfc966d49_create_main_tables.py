"""create main tables
Revision ID: 12345678654
Revises:
Create Date: 2020-05-05 10:41:35.468471
"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "12345678654"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )



def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "added_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )


def create_equities_table() -> None:
    op.create_table(
        "equities",
        sa.Column("ticker", sa.Text, primary_key=True, nullable=False, index=True),
        sa.Column("short_name", sa.Text, nullable=True),
        sa.Column("long_name", sa.Text, nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("currency", sa.Text, nullable=True),
        sa.Column("sector", sa.Text, nullable=True),
        sa.Column("industry", sa.Text, nullable=True),
        sa.Column("exchange", sa.Text, nullable=True),
        sa.Column("market", sa.Text, nullable=True),
        sa.Column("country", sa.Text, nullable=True),
        sa.Column("city", sa.Text, nullable=True),
    )


def create_ETFs_table() -> None:
    op.create_table(
        "etfs",
        sa.Column("ticker", sa.Text, primary_key=True, nullable=False, index=True),
        sa.Column("short_name", sa.Text, nullable=True),
        sa.Column("long_name", sa.Text, nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("currency", sa.Text, nullable=True),
        sa.Column("category", sa.Text, nullable=True),
        sa.Column("family", sa.Text, nullable=True),
        sa.Column("exchange", sa.Text, nullable=True),
        sa.Column("market", sa.Text, nullable=True),
        *timestamps(),
    )




def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email_verified", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="True"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="False"),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_portfolios_table() -> None:
    op.create_table(
        "portfolios",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id'), nullable=False, index=True, ),
        sa.Column("portfolio_weights", sa.JSON, nullable=False),
        sa.Column("returns", sa.Float, nullable=False),
        sa.Column("std", sa.Float, nullable=False),
        sa.Column("sharpe_ratio", sa.Float, nullable=False),
        sa.Column("return_over_risk", sa.Float, nullable=False),
        sa.Column("optimization_type", sa.Text, nullable=False),
        sa.Column("optimization_method", sa.Text, nullable=False),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_portfolio_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )




def upgrade() -> None:
    create_updated_at_trigger()
    create_equities_table()
    create_ETFs_table()
    create_users_table()
    create_portfolios_table()



def downgrade() -> None:
    op.drop_table("equities")
    op.drop_table("etfs")
    op.drop_table("portfolios")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column")

