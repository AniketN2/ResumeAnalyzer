from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os

from prompts.resume_prompt import SYSTEM_PROMPT
from models.candidate import Candidate

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_resume(resume_text):
    try:
        completion = client.responses.parse(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": resume_text,
                },
            ],
            text_format=Candidate,
        )
        return completion.output_parsed

    except OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while parsing resume: {e}")
        return None