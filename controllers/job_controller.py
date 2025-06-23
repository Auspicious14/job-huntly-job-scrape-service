from typing import List
from fastapi import APIRouter
from models.job_models import Payload, JobResponse
from services.scraper_service import scrape_jobs

router = APIRouter()

@router.post("/jobs/scrape", response_model=List[JobResponse])
async def scrape_jobs_controller(payload: Payload):
    """
    Controller handling job scraping requests
    """
    results = scrape_jobs(payload)
    print(results)
    return results
