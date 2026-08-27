import os
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.cloth_analyzer import analyze_cloth
from backend.product_search import search_indian_products
from backend.main import rank_products


app = FastAPI(title="DripSearch AI API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://drip-search-ai.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "DripSearch AI API is running"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    suffix = os.path.splitext(
        file.filename or ""
    )[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp:

        contents = await file.read()

        temp.write(contents)

        temp_path = temp.name

    try:

        cloth_data = analyze_cloth(temp_path)

        if not cloth_data:
            return {
                "error": "AI analysis is temporarily unavailable. Please try again.",
                "analysis": None,
                "products": []
            }

        products = search_indian_products(
            cloth_data["search_query"]
        )

        ranked_products = rank_products(
            products,
            cloth_data
        )

        return {
            "analysis": cloth_data,
            "products": ranked_products
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)