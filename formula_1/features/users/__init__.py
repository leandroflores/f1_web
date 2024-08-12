from fastapi import APIRouter

from .login import router as login_router
from .users_me import router as me_router
from .users import router as users_router

router = APIRouter(tags=["Users"])
router.include_router(login_router)
router.include_router(me_router)
router.include_router(users_router)
