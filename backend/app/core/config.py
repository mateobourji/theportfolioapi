from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")
PROJECT_NAME = "The Portfolio API"
VERSION = "0.1.0"
DESCRIPTION = "The Portfolio (REST) API is used to screen assets across multiple classes, generate quantitative and " \
              "qualitative analysis of these assets, and build optimized portfolios."
API_PREFIX = "/api"
DOCS_URL = "/"
TAGS_META = [
{
    "name": "Authentication",
    "description": "The Portfolio API uses OAuth2 and JWT to authenticate users. Please register or login to consume "
                   "this API's endpoints. "
},
{
    "name": "Screening",
    "description": "Screen assets across different asset classes based on quantitative attributes (such as % of equity"
                   " holdings of ETFs) and qualitative attributes (such as industry or sector of equities)."
},
{
    "name": "Analysis",
    "description": "Generate statistical analysis,"
                   "quantitative and qualitative fundamental analysis of assets. "
},
{
    "name": "Portfolio",
    "description": "Build optimized investment portfolios using modern portfolio theory optimization and monte"
                   "carlo simulation."
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

REDIS_PASSWORD = config("REDIS_PASSWORD", cast=str)
REDIS_SERVER= config("REDIS_SERVER", cast=int)
REDIS_PORT= config("REDIS_PORT", cast=int)
REDIS_HOST= config("REDIS_HOST", cast=str)
