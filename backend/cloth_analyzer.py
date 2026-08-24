import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_cloth(image_path):

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
- clothing_type examples:
  t-shirt, shirt, hoodie, jeans, jacket, dress, kurti, saree, top, trousers, sweater.

- pattern examples:
  plain, striped, checked, floral, graphic print, waffle knit, solid, unknown.

- gender examples:
  men, women, unisex, unknown.

- search_query MUST be a short, specific, shopping-friendly
  description of the clothing item.

Examples:

"black oversized men's t-shirt"
"women rust waffle knit top"
"blue straight fit men's jeans"
"beige oversized hoodie men"

Do NOT use "unknown clothing item" unless absolutely nothing
about the clothing can be determined.
"""

    try:

        # Read the actual image file
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Determine image type
        extension = os.path.splitext(image_path)[1].lower()

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }

        mime_type = mime_types.get(
            extension,
            "image/jpeg"
        )

        # Convert file into an actual Gemini image part
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",

            contents=[
                prompt,
                image_part
            ],

            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json"
            )
        )

        print("\n===== GEMINI RESPONSE =====")
        print(response.text)

        data = json.loads(response.text)

        return data

    except Exception as e:

        print("\n❌ CLOTH ANALYSIS ERROR:")
        print(e)

        return {
            "clothing_type": "unknown",
            "color": "unknown",
            "pattern": "unknown",
            "style": "unknown",
            "gender": "unknown",
            "search_query": "unknown clothing item"
        }