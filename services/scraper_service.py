import logging
from jobspy import scrape_jobs as jobspy_scrape
from models.job_models import Payload, JobResponse
from typing import List
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_jobs(payload: Payload) -> List[JobResponse]:
    try:
        logger.info(f"Starting job scrape for search term: {payload.search_term}")
        jobs = jobspy_scrape(
            site_name=payload.site_name,
            search_term=payload.search_term,
            location=payload.location,
            results_wanted=payload.results_wanted,
            hours_old=payload.hours_old,
            country_indeed=payload.country_indeed
        )
        print(jobs)
        logger.info(f"Successfully scraped {len(jobs)} jobs")
        try:
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
        except Exception as e:
            logger.error(f"Error parsing job data: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error parsing job data: {str(e)}")
    except Exception as e:
        logger.error(f"Error during job scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during job scraping: {str(e)}")