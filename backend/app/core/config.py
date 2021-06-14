from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")
PROJECT_NAME = "The Portfolio API"
VERSION = "0.1.0"
DESCRIPTION = "The Portfolio API is used to screen portfolio investments across multiple asset classes," \
              " analyze historical performance data, and build portfolios through various optimization techniques."
API_PREFIX = "/api"
DOCS_URL = "/"
TAGS_META = [
{
    "name": "screener",
    "description": "Screen assets throughout different asset classes."
},
{
    "name": "historical performance",
    "description": "Get historical performance of a single assets or group of assets. Covers asset prices, dividends,"
                   " returns, summary statistics (returns mean, std, skew, kurtosis) and joint summary statistics"
                   " (returns correlation, covariance)."
},
{
    "name": "portfolio",
    "description": "Build optimized portfolio."
},
    {
    "name": "admin",
    "description": "Add, update, and delete assets in the database."
}
]

SECRET_KEY = config("SECRET_KEY", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    cast=int,
    default=7 * 24 * 60  # one week
)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="PyFolio:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)
DATABASE_URL = config(
  "DATABASE_URL",
  cast=DatabaseURL,
  default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
