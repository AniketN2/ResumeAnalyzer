from pydantic import BaseModel
from typing import List


class ImprovementPlan(BaseModel):
    missing_skills: List[str]
    suggestions: List[str]
    summary: str