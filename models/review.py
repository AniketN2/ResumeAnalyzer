from pydantic import BaseModel
from typing import List


class Review(BaseModel):

    summary: str

    strengths: List[str]

    weaknesses: List[str]

    interview_questions: List[str]

    final_recommendation: str