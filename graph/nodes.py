from utils.pdf_reader import extract_text_from_pdf

from agents.resume_parser import parse_resume
from agents.matching_agent import match_candidate
from agents.scoring_agent import calculate_score
from agents.reviewer_agent import generate_review
from agents.resume_coach_agent import generate_improvement_plan


def resume_parser_node(state):
    text, pages = extract_text_from_pdf(state["pdf_path"])

    candidate = parse_resume(text)

    if candidate is None:
        state["error"] = "Candidate parsing failed."
        return state

    state["candidate"] = candidate
    return state


def matching_node(state):
    if state.get("error"):
        return state

    match = match_candidate(state["candidate"], state["jd"])

    if match is None:
        state["error"] = "Matching failed."
        return state

    state["match"] = match
    return state


def scoring_node(state):
    if state.get("error"):
        return state

    score = calculate_score(state["match"])

    if score is None:
        state["error"] = "Score generation failed."
        return state

    state["score"] = score
    return state


def reviewer_node(state):
    if state.get("error"):
        return state

    review = generate_review(
        state["candidate"],
        state["jd"],
        state["match"],
        state["score"]
    )

    if review is None:
        state["error"] = "Review generation failed."
        return state

    state["review"] = review
    return state


def improvement_node(state):
    if state.get("error"):
        return state

    improvement = generate_improvement_plan(
        state["candidate"],
        state["jd"],
        state["match"],
        state["score"]
    )

    if improvement is None:
        state["error"] = "Improvement plan generation failed."
        return state

    state["improvement"] = improvement
    return state


def route_after_scoring(state):
    if state.get("error"):
        return "end"

    if state["score"].total_score >= 70:
        return "reviewer"

    return "improvement"