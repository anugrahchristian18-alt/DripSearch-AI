# DripSearch AI 🛍️

DripSearch AI is an AI-powered fashion product discovery app that helps users find similar clothing products online by uploading an image.

The app analyzes the uploaded clothing image using a vision model, generates a shopping-friendly search query, searches Indian e-commerce results, and displays matching products with images, prices, store names, ratings when available, and shopping links.

---

## 🚀 Features

- Upload a clothing image
- AI-based clothing analysis using Gemini Vision
- Extracts clothing details such as:
  - Clothing type
  - Color
  - Pattern
  - Style
  - Gender
  - Search query
- Searches similar products using SerpAPI Google Shopping
- Filters results from Indian shopping platforms
- Displays product cards with:
  - Product image
  - Product title
  - Price in INR
  - Store/source name
  - Rating when available
  - Shopping link
- Modern fashion-style Streamlit UI
- Relevance-based product ranking

---

## 🧠 How It Works

1. The user uploads a clothing image.
2. Gemini Vision analyzes the image.
3. The model returns structured JSON containing clothing attributes.
4. A search-friendly query is generated from those attributes.
5. SerpAPI fetches Google Shopping results for India.
6. Results are filtered for Indian shopping platforms.
7. Products are ranked by relevance.
8. The app displays matching products in a clean product-card layout.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini Vision
- SerpAPI
- Google Shopping Results
- Requests
- HTML/CSS for custom UI
- dotenv for environment variables

---

## 📁 Project Structure

```text
AI_FashionProject/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
