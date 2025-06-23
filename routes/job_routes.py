from fastapi import APIRouter
from controllers.job_controller import controllerRouter

router = APIRouter()
router.include_router(controllerRouter, prefix="/api")