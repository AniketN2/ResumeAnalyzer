from models.match_result import MatchResult
import re


def normalize(skills):

    if not skills:
        return set()

    return {
        skill.strip().lower()
        for skill in skills
        if skill and skill.strip()
    }


def parse_required_years(minimum_experience):

    if not minimum_experience:
        return 0.0

    text = str(minimum_experience).lower()

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:-|to|–|—)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        text,
    )
    if range_match:
        return float(range_match.group(1))

    number_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        text,
    )
    if number_match:
        return float(number_match.group(1))

    fallback_number = re.search(r"(\d+(?:\.\d+)?)", text)
    if fallback_number:
        return float(fallback_number.group(1))

    return 0.0


def estimate_candidate_years(candidate):

    if candidate is None:
        return 0.0

    structured_years = getattr(candidate, "years_of_experience", None)
    if structured_years is not None:
        try:
            return max(float(structured_years), 0.0)
        except (TypeError, ValueError):
            pass

    years_found = []

    for item in getattr(candidate, "experience", []) or []:
        text = str(item).lower()

        range_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:-|to|–|—)\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            text,
        )
        if range_match:
            years_found.append(float(range_match.group(2)))
            continue

        number_match = re.search(
            r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
            text,
        )
        if number_match:
            years_found.append(float(number_match.group(1)))

    if years_found:
        return max(years_found)

    return 0.0


def match_candidate(candidate, jd):

    if candidate is None or jd is None:
        return MatchResult(
            matched_skills=[],
            missing_skills=[],
            extra_skills=[],
            skill_match_percentage=0.0,
            experience_match=False,
            required_experience_years=0.0,
            candidate_experience_years=0.0,
            experience_gap_years=0.0,
            education_match=False,
        )

    candidate_skills = normalize(getattr(candidate, "skills", []))

    required_skills = normalize(getattr(jd, "required_skills", []))

    matched = candidate_skills & required_skills

    missing = required_skills - candidate_skills

    extra = candidate_skills - required_skills

    if len(required_skills) == 0:
        percentage = 0
    else:
        percentage = (
            len(matched) / len(required_skills)
        ) * 100

    required_experience_years = parse_required_years(
        getattr(jd, "minimum_experience", "")
    )

    candidate_experience_years = estimate_candidate_years(candidate)

    experience_match = candidate_experience_years >= required_experience_years

    experience_gap_years = round(
        candidate_experience_years - required_experience_years,
        2,
    )

    education_match = False

    if getattr(candidate, "education", None) and getattr(jd, "education", None):
        education_match = True

    return MatchResult(

        matched_skills=sorted(list(matched)),

        missing_skills=sorted(list(missing)),

        extra_skills=sorted(list(extra)),

        skill_match_percentage=round(
            percentage,
            2
        ),

        experience_match=experience_match,

        required_experience_years=round(
            required_experience_years,
            2,
        ),

        candidate_experience_years=round(
            candidate_experience_years,
            2,
        ),

        experience_gap_years=experience_gap_years,

        education_match=education_match
    )