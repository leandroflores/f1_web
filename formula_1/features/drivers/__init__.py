from fastapi import APIRouter

from .drivers import router as drivers_router

router = APIRouter(tags=["Driver"])
router.include_router(drivers_router)
