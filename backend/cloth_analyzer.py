import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_cloth(image_path, max_retries=3):

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

- If unsure about one attribute, use "unknown" for that attribute.
- Do not guess brand.
- clothing_type examples:
  t-shirt, shirt, hoodie, jeans, jacket, dress, kurti, saree, top, trousers, sweater, blazer.

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
"black women's formal blazer"

Do NOT use "unknown clothing item" unless absolutely nothing
about the clothing can be determined.
"""

    try:

        # Read image
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # Determine MIME type
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

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        # Retry temporary Gemini failures
        for attempt in range(max_retries):

            try:

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

                error_text = str(e)

                # Retry only temporary API failures
                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                ):

                    if attempt < max_retries - 1:

                        wait_time = 2 ** attempt

                        print(
                            f"\n⚠️ Gemini temporarily unavailable."
                            f" Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                    else:

                        print(
                            "\n❌ Gemini failed after all retries:"
                        )
                        print(e)

                        return {
                            "clothing_type": "unknown",
                            "color": "unknown",
                            "pattern": "unknown",
                            "style": "unknown",
                            "gender": "unknown",
                            "search_query": "unknown clothing item"
                        }

                else:

                    # Non-temporary error
                    print(
                        "\n❌ GEMINI ERROR:"
                    )
                    print(e)

                    return {
                        "clothing_type": "unknown",
                        "color": "unknown",
                        "pattern": "unknown",
                        "style": "unknown",
                        "gender": "unknown",
                        "search_query": "unknown clothing item"
                    }

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