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


def analyze_cloth(image_path, max_retries=1):

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

- Identify the clothing item as accurately as possible.
- If one specific attribute is genuinely impossible to determine,
  use "unknown" ONLY for that attribute.
- Do NOT return all attributes as "unknown" unless the image
  contains no recognizable clothing.
- Do not guess brand.
- clothing_type examples:
  t-shirt, shirt, hoodie, jeans, jacket, dress, kurti, saree,
  top, trousers, sweater, blazer.

- pattern examples:
  plain, striped, checked, floral, graphic print,
  waffle knit, solid, unknown.

- gender examples:
  men, women, unisex, unknown.

- style examples:
  casual, formal, oversized, slim-fit, relaxed, streetwear,
  sporty, traditional, unknown.

- search_query MUST be a short, specific, shopping-friendly
  description using the attributes you can confidently identify.

Examples:

"plain red t-shirt"
"black oversized men's t-shirt"
"women rust waffle knit top"
"blue straight fit men's jeans"
"beige oversized hoodie men"
"black women's formal blazer"

IMPORTANT:
For a simple clearly visible item such as a plain red t-shirt,
the expected result should contain:
clothing_type = "t-shirt"
color = "red"
pattern = "plain" or "solid"

Do NOT use "unknown clothing item" as the search query.
If the image contains recognizable clothing, create the best
possible shopping query from the visible attributes.
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

        # Create Gemini image part
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        # Try once + one retry for temporary failures
        for attempt in range(max_retries + 1):

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

                temporary_error = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                )

                if temporary_error and attempt < max_retries:

                    print(
                        "\n⚠️ Gemini temporarily unavailable."
                        " Retrying once..."
                    )

                    time.sleep(1)

                    continue

                print("\n❌ GEMINI ANALYSIS FAILED:")
                print(e)

                return None

    except Exception as e:

        print("\n❌ CLOTH ANALYSIS ERROR:")
        print(e)

        return None