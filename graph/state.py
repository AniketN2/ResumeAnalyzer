from typing import TypedDict, Optional

from models.candidate import Candidate
from models.job_description import JobDescription
from models.match_result import MatchResult
from models.score import Score
from models.review import Review
from models.improvement import ImprovementPlan


class GraphState(TypedDict):
    pdf_path: str
    candidate: Optional[Candidate]
    jd: JobDescription
    match: Optional[MatchResult]
    score: Optional[Score]
    review: Optional[Review]
    improvement: Optional[ImprovementPlan]
    error: Optional[str]