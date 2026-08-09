import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts.reviewer_prompt import SYSTEM_PROMPT
from models.review import Review

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_review(
    candidate,
    jd,
    match_result,
    score
):

    prompt = f"""
Candidate:

{candidate.model_dump_json(indent=2)}

Job Description:

{jd.model_dump_json(indent=2)}

Match Result:

{match_result.model_dump_json(indent=2)}

Score:

{score.model_dump_json(indent=2)}
"""

    response = client.responses.parse(

        model="gpt-4.1-mini",

        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        text_format=Review
    )

    return response.output_parsed