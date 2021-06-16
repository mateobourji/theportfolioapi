from fastapi import APIRouter
from backend.app.api.routes.historical_performance import router as download_router
from backend.app.api.routes.portfolio import router as portfolio_router
from backend.app.api.routes.screener import router as screener_router
from backend.app.api.routes.admin import router as asset_router
from backend.app.api.routes.users import router as user_router
router = APIRouter()


router.include_router(screener_router, prefix="/screener", tags=["screener"])
router.include_router(download_router, prefix="/historical-performance", tags=["historical performance"])
router.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])
router.include_router(asset_router, prefix="/admin", tags=["admin"])
router.include_router(user_router, prefix="/users", tags=["users"])