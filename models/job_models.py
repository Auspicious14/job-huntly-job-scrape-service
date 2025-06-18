from pydantic import BaseModel

class Payload(BaseModel):
    site_name: list[str]
    search_term: str
    google_search_term: str
    location: str
    results_wanted: int
    hours_old: int
    country_indeed: str
    is_remote: bool
    job_type: str

class JobResponse(BaseModel):
    title: str
    company: str
    company_url: str | None
    job_url: str
    location: dict[str, str | None]
    is_remote: bool
    description: str
    job_type: str
    salary: dict[str, str | float | None]
    date_posted: str
    emails: list[str] | None