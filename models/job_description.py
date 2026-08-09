from pydantic import BaseModel
from typing import List


class JobDescription(BaseModel):
    job_title: str
    required_skills: List[str]
    preferred_skills: List[str]
    minimum_experience: str
    education: List[str]
    responsibilities: List[str]