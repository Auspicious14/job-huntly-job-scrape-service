import logging
from jobspy import scrape_jobs as jobspy_scrape
from models.job_models import Payload, JobResponse
from typing import List, Tuple
from fastapi import HTTPException, Query
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_jobs(
    site_name: str = Query(...),
    search_term: str = Query(...),
    location: str = Query(None),
    results_wanted: int = Query(10),
    hours_old: int = Query(None),
    country_indeed: str = Query(None),
    is_remote: bool = Query(None),
    job_type: str = Query(None)
):
    df: pd.DataFrame = jobspy_scrape(
        site_name=site_name.split(","),
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
        country_indeed=country_indeed,
        is_remote=is_remote,
        job_type=job_type
    )
    jobs = df.to_dict(orient="records")
    # Optional: convert pandas types to JSON-compatible
    for job in jobs:
        for k, v in job.items():
            if pd.isna(v):
                job[k] = None
    return {"success": True, "jobs": jobs, "returned_results": len(jobs)}

    logger.info(f"Starting job scrape for search term: {payload.search_term}")