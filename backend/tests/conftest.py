import warnings
import os
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
import alembic
from alembic.config import Config
from typing import List
from backend.app.models.user import UserCreate, UserInDB
from backend.app.db.repositories.users import UsersRepository
from backend.app.models.ticker import TickerInDB
from backend.app.models.equity import EquityCreate, EquityInDB
from backend.app.db.repositories.assets import SecuritiesRepository
from backend.app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX
from backend.app.services import auth_service


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from backend.app.api.server import get_application
    return get_application()


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return backend.app.state._db


# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
                app=app,
                base_url="http://testserver",
                headers={"Content-Type": "application/json"}
        ) as client:
            yield client


# Mock cleaning data for our tests


@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="lebron@james.io",
        username="lebronjames",
        password="heatcavslakers",
    )
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)

@pytest.fixture
async def test_user_new(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="shakira@hips.com",
        username="shakira",
        password="shark-ira",
    )
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)

@pytest.fixture
def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client


@pytest.fixture
def authorized_client_new(client: AsyncClient, test_user_new: UserInDB) -> AsyncClient:
    access_token = auth_service.create_access_token_for_user(user=test_user_new, secret_key=str(SECRET_KEY))
    client.headers = {
        **client.headers,
        "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}",
    }
    return client

@pytest.fixture
async def test_equities1(db: Database) -> List[EquityInDB]:
    equities = [EquityInDB(ticker='CSCO',
                           name='Cisco Systems, Inc.',
                           country='United States',
                           sector='Technology',
                           industry='Communication Equipment',
                           exchange='NMS'),
                EquityInDB(ticker='NFLX',
                           name='Netflix, Inc.',
                           country='United States',
                           sector='Communication Services',
                           industry='Entertainment',
                           exchange='NMS'),
                EquityInDB(ticker="AAPL",
                           name="Apple Inc.",
                           country="United States",
                           sector="Technology",
                           industry="Consumer Electronics",
                           exchange="NMS"),
                EquityInDB(ticker="AMZN",
                           name="Amazon.com, Inc.",
                           country="United States",
                           sector="Consumer Cyclical",
                           industry="Internet Retail",
                           exchange="NMS"),
                EquityInDB(ticker="BP",
                           name="BP p.l.c.",
                           country="United Kingdom",
                           sector="Energy",
                           industry="Oil & Gas Integrated",
                           exchange="NYQ")
                ]

    await SecuritiesRepository(db).add_tickers(tickers=[equity.ticker for equity in equities])

    return equities
