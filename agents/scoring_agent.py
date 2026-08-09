from models.score import Score


def calculate_score(match_result):

    # -------- Skills --------

    skill_score = (
        match_result.skill_match_percentage * 0.60
    )

    # -------- Experience --------

    experience_score = (
        25 if match_result.experience_match else 0
    )

    # -------- Education --------

    education_score = (
        15 if match_result.education_match else 0
    )

    total = (
        skill_score
        + experience_score
        + education_score
    )

    if total >= 85:
        recommendation = "Strong Hire"

    elif total >= 70:
        recommendation = "Interview"

    elif total >= 50:
        recommendation = "Consider"

    else:
        recommendation = "Reject"

    return Score(

        skill_score=round(skill_score,2),

        experience_score=experience_score,

        education_score=education_score,

        total_score=round(total,2),

        recommendation=recommendation
    )