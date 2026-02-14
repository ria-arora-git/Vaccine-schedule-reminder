import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def parse_vaccine_text(raw_text):
    prompt = f"""
    Extract vaccine schedule information from this text.

    Return ONLY valid JSON.
    No explanation.

    Format:

    [
      {{
        "vaccine_name": "string",
        "due_age_weeks": number
      }}
    ]

    Text:
    {raw_text}
    """

    response = model.generate_content(prompt)

    text_output = response.text.strip()

    if text_output.startswith("```"):
        text_output = text_output.replace("```json", "").replace("```", "").strip()

    return json.loads(text_output)
