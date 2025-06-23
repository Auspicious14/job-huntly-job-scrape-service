from fastapi import APIRouter
from controllers.job_controller import router

router = APIRouter()
router.include_router(router, prefix="/api")