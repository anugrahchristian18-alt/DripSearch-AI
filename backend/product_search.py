import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_indian_products(query, max_results=8):
    if not SERPAPI_KEY:
        print("❌ SERPAPI_KEY not found in .env")
        return []

    url = "https://serpapi.com/search"

    params = {
        "engine": "google_shopping",
        "q": query,
        "gl": "in",
        "hl": "en",
        "location": "India",
        "direct_link": "true",
        "api_key": SERPAPI_KEY,
    }

    response = requests.get(url, params=params)

    print("STATUS CODE:", response.status_code)

    data = response.json()

    print("SERPAPI RESPONSE KEYS:", data.keys())

    if "error" in data:
        print("SERPAPI ERROR:", data["error"])
        return []

    shopping_results = data.get("shopping_results", [])

    print("SHOPPING RESULTS COUNT:", len(shopping_results))

    if len(shopping_results) == 0:
        print("FULL SERPAPI RESPONSE:")
        print(data)
        return []

    products = []

    for item in shopping_results[:max_results]:
        products.append({
            "title": item.get("title", "No title"),
            "price": item.get("price", "Price not available"),
            "source": item.get("source", "Unknown"),
            "image": item.get("thumbnail") or item.get("serpapi_thumbnail"),
            "link": item.get("product_link") or item.get("link"),
            
            "rating": item.get("rating","N/A"),
            "reviews": item.get("reviews","N/A")
        })

    return products