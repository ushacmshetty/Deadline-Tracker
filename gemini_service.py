import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def extract_deadlines(image_bytes, mime_type, prompt):

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            prompt,
            image_part
        ]
    )

    return json.loads(response.text)