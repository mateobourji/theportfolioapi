from fastapi import APIRouter
from app.api.routes.download_data import router as download_router
from app.api.routes.security_stats import router as stats_router
from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.securities import router as ticker_router

router = APIRouter()
router.include_router(ticker_router, prefix="/screener", tags=["screener"])
router.include_router(download_router, prefix="/download-data", tags=["data"])
router.include_router(stats_router, prefix="/download-stats", tags=["statistics"])
router.include_router(portfolio_router, prefix="/portfolio", tags=["statistics"])
