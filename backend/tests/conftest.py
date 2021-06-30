import json
import random
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

from app.models.etf import ETFInDB
from app.models.fund import FundInDB
from app.models.user import UserCreate, UserInDB
from app.db.repositories.users import UsersRepository
from app.models.ticker import TickerInDB
from app.models.equity import EquityCreate, EquityInDB
from app.db.repositories.equity import EquityRepository
from app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX
from app.services import auth_service


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
    from app.api.server import get_application
    return get_application()


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


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
async def test_equities(db: Database) -> List[EquityInDB]:
    file = os.fsencode('app/db/migrations/data/Equities/equities_part1.json')
    with open(file) as json_file:
        data = json.load(json_file)
        equities = []
        for asset in random.choices(list(data), k=10):
            try:
                data[asset]['ticker'] = asset
                equities.append(EquityInDB.parse_obj(data[asset]))
            except:
                continue
    return equities


@pytest.fixture
async def test_etfs(db: Database) -> List[ETFInDB]:
    file = os.fsencode('app/db/migrations/data/ETFs/World Allocation.json')
    with open(file) as json_file:
        data = json.load(json_file)
        etfs = []
        for asset in random.choices(list(data), k=10):
            try:
                data[asset]['ticker'] = asset
                etfs.append(ETFInDB.parse_obj(data[asset]))
            except:
                continue
    return etfs


@pytest.fixture
async def test_funds(db: Database) -> List[FundInDB]:
    file = os.fsencode('app/db/migrations/data/Funds/Diversified Emerging Mkts.json')
    with open(file) as json_file:
        data = json.load(json_file)
        funds = []
        for asset in random.choices(list(data), k=10):
            try:
                data[asset]['ticker'] = asset
                funds.append(FundInDB.parse_obj(data[asset]))
            except:
                continue
    return funds
