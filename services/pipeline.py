# from utils.pdf_reader import extract_text_from_pdf

# from agents.resume_parser import parse_resume
# from agents.matching_agent import match_candidate
# from agents.scoring_agent import calculate_score
# from agents.reviewer_agent import generate_review


# def process_resume(pdf_path, jd):

#     text, pages = extract_text_from_pdf(pdf_path)

#     candidate = parse_resume(text)

#     if candidate is None:
#         raise Exception("Candidate parsing failed.")

#     match = match_candidate(candidate, jd)

#     if match is None:
#         raise Exception("Matching failed.")

#     score = calculate_score(match)

#     if score is None:
#         raise Exception("Score generation failed.")

#     review = generate_review(
#         candidate,
#         jd,
#         match,
#         score
#     )

#     if review is None:
#         raise Exception("Review generation failed.")

#     return {
#         "candidate": candidate,
#         "match": match,
#         "score": score,
#         "review": review
#     }


# Version 2: Using the graph-based pipeline
from graph.graph import resume_graph


def process_resume(pdf_path, jd):

    initial_state = {
        "pdf_path": pdf_path,
        "candidate": None,
        "jd": jd,
        "match": None,
        "score": None,
        "review": None,
        "improvement": None,
        "error": None
    }

    final_state = resume_graph.invoke(initial_state)

    if final_state.get("error"):
        raise Exception(final_state["error"])

    return final_state