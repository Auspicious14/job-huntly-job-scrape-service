import logging
from jobspy import scrape_jobs as jobspy_scrape
from models.job_models import Payload, JobResponse
from typing import List
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_jobs(payload: Payload) -> List[JobResponse]:
    logger.info(f"Starting job scrape for search term: {payload.search_term}")
    jobs = jobspy_scrape(
        site_name=payload.site_name,
        search_term=payload.search_term,
        google_search_term: payload.google_search_term,
        location=payload.location,
        results_wanted=payload.results_wanted,
        hours_old=payload.hours_old,
        country_indeed=payload.country_indeed,
        is_remote=payload.is_remote,
        job_type=payload.job_type
    )
    logger.info(f"Successfully scraped {len(jobs)} jobs")
    logger.info(f"Type of jobs: {type(jobs)}; First job: {jobs[0] if jobs else 'None'}")
    job_responses = []
    for job in jobs:
        if isinstance(job, dict):
            job_responses.append(JobResponse(**job))
        elif hasattr(job, 'dict'):
            job_responses.append(JobResponse(**job.dict()))
        else:
            logger.error(f"Job is not a dict or pydantic model: {job}")
    return job_responses