from fastapi import APIRouter, Depends

from app.users.dependencies import has_perm, get_current_user
from app.users.models import User
from .routes.role import router as role_router
from .routes.user import router as user_router
router = APIRouter()
router.include_router(role_router)
router.include_router(user_router)