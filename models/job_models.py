from typing import Optional, Dict, List, Union
from pydantic import BaseModel

class JobResponse(BaseModel):
    title: str
    company: str
    company_url: Optional[str]
    job_url: str
    location: Dict[str, Optional[str]]
    is_remote: bool
    description: str
    job_type: str
    salary: Dict[str, Optional[Union[str, float]]]
    date_posted: str
    emails: Optional[List[str]]

    class Config:
        json_encoders = {
            float: lambda v: str(v) if v is not None else None
        }
        allow_population_by_field_name = True
