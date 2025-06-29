import logging
from jobspy import scrape_jobs as jobspy_scrape
from models.job_models import Payload, JobResponse
from typing import List, Tuple
from fastapi import HTTPException
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_jobs(payload: Payload) -> dict:
    df: pd.DataFrame = jobspy_scrape(
        site_name=payload.site_name,
        search_term=payload.search_term,
        location=payload.location,
        results_wanted=payload.results_wanted,
        hours_old=payload.hours_old,
        country_indeed=payload.country_indeed,
        is_remote=payload.is_remote,
        job_type=payload.job_type
    )
    jobs = df.to_dict(orient="records")
    # Optional: convert pandas types to JSON-compatible
    for job in jobs:
        for k, v in job.items():
            if pd.isna(v):
                job[k] = None
    logger.info(f"Starting job scrape for search term: {payload.search_term}")
    return {"success": True, "jobs": jobs, "returned_results": len(jobs)}