from pydantic import BaseModel
from typing import List


class Score(BaseModel):

    skill_score: float

    experience_score: float

    education_score: float

    total_score: float

    recommendation: str