from fastapi import APIRouter

from .companies import router as companies_router

router = APIRouter(tags=["Company"])
router.include_router(companies_router)
