import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_cloth(image):
    prompt = """
You are a fashion product tagging system for an online shopping app.

Look ONLY at the visible clothing item in the image.
Identify the MAIN clothing item, not the background or person.

Return ONLY valid JSON. No markdown. No explanation.

JSON format:
{
  "clothing_type": "",
  "color": "",
  "pattern": "",
  "style": "",
  "gender": "",
  "search_query": ""
}

Rules:
- If unsure, use "unknown".
- Do not guess brand.
- clothing_type examples: t-shirt, shirt, hoodie, jeans, jacket, dress, kurti, saree, top.
- pattern examples: plain, striped, checked, floral, graphic print, waffle knit, unknown.
- gender examples: men, women, unisex, unknown.
- search_query must be short and shopping-friendly.
Example: "women rust waffle knit quarter zip short sleeve top"
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image],
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "clothing_type": "unknown",
            "color": "unknown",
            "pattern": "unknown",
            "style": "unknown",
            "gender": "unknown",
            "search_query": "unknown clothing item"
        }