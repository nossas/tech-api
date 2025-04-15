from fastapi import APIRouter

from ..api.calendar import router as calendar_router

router = APIRouter(prefix="/api")
router.include_router(calendar_router)