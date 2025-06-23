from jobspy import scrape_jobs
from models.job_models import Payload, JobResponse

def scrape_jobs(payload: Payload) -> list[JobResponse]:
    return [JobResponse(**job.dict()) for job in scrape_jobs(payload)]