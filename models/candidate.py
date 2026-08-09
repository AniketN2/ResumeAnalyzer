from pydantic import BaseModel
from typing import List, Optional


class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    skills: List[str]
    education: List[str]
    experience: List[str]
    years_of_experience: Optional[float] = None
    projects: List[str]
    linkedin: str
    github: str
    certifications: List[str]
    languages: List[str]