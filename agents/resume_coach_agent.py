from langchain_openai import ChatOpenAI
from models.improvement import ImprovementPlan

SYSTEM_PROMPT = """
You are a professional resume coach.

You will be given:
- The candidate's resume details
- The list of missing skills compared to the job description
- The candidate's score

Your job is to generate a helpful, encouraging resume improvement plan.

Return only structured data:
- missing_skills: list of missing skills
- suggestions: 3-5 concrete, actionable improvement suggestions
- summary: a short 2-3 sentence summary of what to focus on

Do not explain anything else.
"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(ImprovementPlan)


def generate_improvement_plan(candidate, jd, match, score):
    try:
        user_prompt = f"""
        Candidate Name: {candidate.name}

        Job Title: {jd.job_title}

        Missing Skills: {match.missing_skills}

        Matched Skills: {match.matched_skills}

        Score: {score.total_score}

        Recommendation: {score.recommendation}
        """

        result = structured_llm.invoke([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ])

        return result

    except Exception as e:
        print(f"Error generating improvement plan: {e}")
        return None