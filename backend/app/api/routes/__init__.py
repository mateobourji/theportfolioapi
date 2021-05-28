from fastapi import APIRouter
from app.api.routes.download_data import router as download_router
from app.api.routes.security_stats import router as stats_router
from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.screener import router as screener_router
from app.api.routes.assets import router as asset_router
router = APIRouter()

router.include_router(asset_router, prefix="/assets", tags=["assets"])
router.include_router(screener_router, prefix="/screener", tags=["screener"])
router.include_router(download_router, prefix="/download-data", tags=["historical performance"])
router.include_router(stats_router, prefix="/download-stats", tags=["historical performance"])
router.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])
