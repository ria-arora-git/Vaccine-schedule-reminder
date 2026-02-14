import requests
import os
from dotenv import load_dotenv

load_dotenv()
OCR_API_KEY = os.getenv("OCR_API_KEY")

def extract_text(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": f},
            data={"apikey": OCR_API_KEY}
        )
    result = response.json()
    return result["ParsedResults"][0]["ParsedText"]
