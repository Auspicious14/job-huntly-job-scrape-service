import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.job_models import Payload, JobResponse
from services.scraper_service import scrape_jobs

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/scrape", 
           response_model=None,
           status_code=status.HTTP_200_OK,
           responses={
               500: {"description": "Internal server error"},
               422: {"description": "Validation error"}
           })
async def scrape_jobs_controller(payload: Payload) -> Any:
    """
    Controller handling job scraping requests
    Args:
        payload (Payload): Job search parameters
    Returns:
        Dict[str, Any]: Dict with scraped jobs and errors
    Raises:
        HTTPException: If there's an error during scraping or validation
    """
    try:
        logger.info(f"Received scraping request for {payload.search_term} in {payload.location}")
        if not payload.site_name:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one site name must be provided"
            )
        service_response = scrape_jobs(payload)
        jobs = service_response.get("jobs", [])
        errors = service_response.get("errors", [])
        logger.info(f"Successfully returned {len(jobs)} jobs with {len(errors)} errors")
        return JSONResponse(content={"jobs": jobs, "errors": errors, "success": service_response.get("success", False), "returned_results": service_response.get("returned_results", 0)}, status_code=200)
    except HTTPException as he:
        logger.error(f"HTTP error in controller: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in controller: {str(e)}")
        return JSONResponse(content={"jobs": [], "errors": [f"Unexpected error: {str(e)}"]}, status_code=500)
