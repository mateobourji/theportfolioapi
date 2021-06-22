from fastapi import APIRouter
from app.api.routes.analysis import router as download_router
from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.screening import router as screener_router
from app.api.routes.admin import router as asset_router
from app.api.routes.authentication import router as user_router
router = APIRouter()

router.include_router(user_router, prefix="/authentication", tags=["Authentication"])
router.include_router(screener_router, prefix="/screener", tags=["Screening"])
router.include_router(download_router, prefix="/analysis", tags=["Analysis"])
router.include_router(portfolio_router, prefix="/portfolio", tags=["Portfolio"])
router.include_router(asset_router, prefix="/admin")
