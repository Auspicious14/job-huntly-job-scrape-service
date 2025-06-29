import logging
from jobspy import scrape_jobs as jobspy_scrape
from models.job_models import Payload, JobResponse
from typing import List, Tuple
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_jobs(payload: Payload) -> Tuple[List[JobResponse], List[str]]:
    logger.info(f"Starting job scrape for search term: {payload.search_term}")
    errors = []
    try:
        jobs = jobspy_scrape(
            site_name=payload.site_name,
            search_term=payload.search_term,
            google_search_term=payload.google_search_term,
            location=payload.location,
            results_wanted=payload.results_wanted,
            hours_old=payload.hours_old,
            country_indeed=payload.country_indeed,
            is_remote=payload.is_remote,
            job_type=payload.job_type
        )
        logger.info(f"Successfully scraped {len(jobs)} jobs")
        logger.info(f"Type of jobs: {type(jobs)}; First job: {jobs[0] if jobs else 'None'}")
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        errors.append(f"Scraping error: {str(e)}")
        jobs = []
    job_responses = []
    for job in jobs:
        try:
            if isinstance(job, dict):
                job_responses.append(JobResponse(**job))
            elif hasattr(job, 'dict'):
                job_responses.append(JobResponse(**job.dict()))
            else:
                msg = f"Job is not a dict or pydantic model: {job}"
                logger.error(msg)
                errors.append(msg)
        except Exception as e:
            msg = f"Error parsing job: {str(e)}"
            logger.error(msg)
            errors.append(msg)
    return job_responses, errors