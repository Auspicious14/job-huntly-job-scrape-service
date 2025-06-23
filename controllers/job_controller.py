from typing import List
from fastapi import APIRouter
from models.job_models import Payload, JobResponse
from services.scraper_service import scrape_jobs

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/scrape", response_model=List[JobResponse])
async def scrape_jobs_controller(payload: Payload):
    """
    Controller handling job scraping requests
    """
    return scrape_jobs(payload)