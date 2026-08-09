from openai import OpenAI
from dotenv import load_dotenv
import os

from prompts.jd_prompt import SYSTEM_PROMPT
from models.job_description import JobDescription

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def parse_job_description(job_description):

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": job_description
            }
        ],
        text_format=JobDescription
    )

    return response.output_parsed