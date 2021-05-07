import warnings
import os
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
import alembic
from alembic.config import Config
from app.models.cleaning import CleaningCreate, CleaningInDB
from app.db.repositories.cleanings import CleaningsRepository
from app.models.user import UserCreate, UserInDB
from app.models.security import EquityCreate, EquityInDB, SecurityInDB
from app.db.repositories.securities import SecuritiesRepository

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
async def test_cleaning(db: Database) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        cleaning_type="spot_clean",
    )
    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning)

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
async def test_equity1(db: Database) -> EquityInDB:
    new_equity = EquityCreate(
        ticker="TEST",
        name="Test Name",
        country="Test Country",
        summary="Test summary.",
        sector="Test Sector",
        industry="Test Industry",
        exchange="TestExchange"
    )
    security_repo = SecuritiesRepository(db)

    return await security_repo.add_equity(new_equity=new_equity)

@pytest.fixture
async def test_equity2(db: Database) -> EquityInDB:
    new_equity = EquityCreate(
        ticker="TEST2",
        name="Test Name2",
        country="Test Country2",
        summary="Test summary2.",
        sector="Test Sector2",
        industry="Test Industry2",
        exchange="TestExchange2"
    )
    security_repo = SecuritiesRepository(db)

    return await security_repo.add_equity(new_equity=new_equity)
