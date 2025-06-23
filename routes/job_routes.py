from fastapi import APIRouter
from controllers.job_controller import router as job_router

router = APIRouter(prefix="/api/jobs")
router.include_router(job_router)