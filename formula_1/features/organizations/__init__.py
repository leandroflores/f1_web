from fastapi import APIRouter

from .organizations import router as organizations_router

router = APIRouter(tags=["Organization"])
router.include_router(organizations_router)
