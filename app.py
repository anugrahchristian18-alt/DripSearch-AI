import streamlit as st
import json
import os
import requests
import html
from dotenv import load_dotenv

load_dotenv()

# ─── Session State ─────────────────────────────────────────────────────────────
if "cloth_data" not in st.session_state:
    st.session_state.cloth_data = None

if "products" not in st.session_state:
    st.session_state.products = []

if "ranked_products" not in st.session_state:
    st.session_state.ranked_products = []


# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StyleFinder AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.stApp {
    background: #0a0a0f;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"] {
    display: none;
}

.hero {
    background: linear-gradient(135deg, #0a0a0f 0%, #12121a 50%, #0a0a0f 100%);
    border-bottom: 1px solid rgba(255,215,100,0.15);
    padding: 3rem 4rem 2.5rem;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -20%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(255,215,100,0.06) 0%, transparent 70%);
    pointer-events: none;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: -40%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(200,100,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,215,100,0.1);
    border: 1px solid rgba(255,215,100,0.3);
    color: #ffd764;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    font-weight: 900;
    color: #f5f0e8;
    line-height: 1.05;
    margin-bottom: 0.6rem;
    letter-spacing: -0.02em;
}

.hero-title span {
    background: linear-gradient(90deg, #ffd764, #ff9f43);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    color: rgba(245,240,232,0.45);
    font-size: 1rem;
    font-weight: 300;
    letter-spacing: 0.02em;
    max-width: 520px;
    line-height: 1.6;
}

.panel-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3);
    margin-bottom: 1.2rem;
}

.analysis-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}

.analysis-title {
    font-family: 'Playfair Display', serif;
    color: #f5f0e8;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.7);
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.3rem 0.7rem;
    border-radius: 8px;
}

.tag.gold {
    background: rgba(255,215,100,0.1);
    border-color: rgba(255,215,100,0.3);
    color: #ffd764;
}

.tag-key {
    color: rgba(255,255,255,0.35);
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-right: 0.25rem;
}

.query-box {
    background: rgba(255,215,100,0.07);
    border: 1px solid rgba(255,215,100,0.2);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-top: 1rem;
}

.query-box p {
    color: rgba(255,255,255,0.4);
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}

.query-box span {
    color: #ffd764;
    font-size: 0.85rem;
    font-style: italic;
}

.results-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.results-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f5f0e8;
}

.results-count {
    color: rgba(255,255,255,0.3);
    font-size: 0.8rem;
}

.product-card {
    background: #12121a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    overflow: hidden;
    transition: all 0.3s ease;
    position: relative;
    margin-bottom: 1.2rem;
}

.product-card:hover {
    border-color: rgba(255,215,100,0.3);
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,215,100,0.1);
}

.card-image-wrap {
    position: relative;
    aspect-ratio: 3/4;
    overflow: hidden;
    background: #1a1a24;
}

.card-image-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.product-card:hover .card-image-wrap img {
    transform: scale(1.06);
}

.source-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    backdrop-filter: blur(10px);
    max-width: 120px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.badge-amazon {
    background: rgba(255,153,0,0.9);
    color: #000;
}

.badge-flipkart {
    background: rgba(47,116,255,0.9);
    color: #fff;
}

.badge-myntra {
    background: rgba(255,63,108,0.9);
    color: #fff;
}

.badge-meesho {
    background: rgba(155,81,224,0.9);
    color: #fff;
}

.badge-nykaa {
    background: rgba(252,66,123,0.9);
    color: #fff;
}

.badge-ajio {
    background: rgba(0,0,0,0.85);
    color: #fff;
    border: 1px solid rgba(255,255,255,0.3);
}

.badge-default {
    background: rgba(30,30,40,0.9);
    color: rgba(255,255,255,0.7);
    border: 1px solid rgba(255,255,255,0.1);
}

.score-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    min-width: 32px;
    height: 32px;
    padding: 0 0.4rem;
    border-radius: 50%;
    background: rgba(255,215,100,0.15);
    border: 1px solid rgba(255,215,100,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
    color: #ffd764;
    backdrop-filter: blur(6px);
}

.card-body {
    padding: 1rem;
}

.card-title {
    color: rgba(255,255,255,0.82);
    font-size: 0.8rem;
    font-weight: 500;
    line-height: 1.4;
    margin-bottom: 0.7rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 2.24em;
}

.card-price {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffd764;
    margin-bottom: 0.8rem;
}

.card-rating {
    color: rgba(255,255,255,0.55);
    font-size: 0.72rem;
    font-weight: 500;
    margin-bottom: 0.8rem;
}

.card-btn {
    display: block;
    width: 100%;
    background: linear-gradient(135deg, #ffd764, #ff9f43);
    color: #0a0a0f !important;
    text-decoration: none !important;
    text-align: center;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.6rem;
    border-radius: 10px;
    transition: all 0.2s ease;
}

.card-btn:hover {
    opacity: 0.9;
    transform: scale(0.98);
    text-decoration: none !important;
    color: #0a0a0f !important;
}

.empty-state {
    text-align: center;
    padding: 5rem 2rem;
    color: rgba(255,255,255,0.2);
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    display: block;
    opacity: 0.4;
}

.empty-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: rgba(255,255,255,0.3);
    margin-bottom: 0.5rem;
}

.empty-sub {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.15);
}

.stFileUploader {
    background: transparent !important;
}

.stFileUploader > div {
    background: rgba(255,215,100,0.04) !important;
    border: 2px dashed rgba(255,215,100,0.25) !important;
    border-radius: 16px !important;
}

.stFileUploader label {
    color: rgba(255,255,255,0.5) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #ffd764, #ff9f43) !important;
    color: #0a0a0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    transform: scale(0.98) !important;
}

.stSpinner > div {
    color: #ffd764 !important;
}

div[data-testid="stImage"] img {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
}

.stImage {
    margin-bottom: 1rem !important;
}

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #0a0a0f;
}

::-webkit-scrollbar-thumb {
    background: rgba(255,215,100,0.2);
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)


# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Fashion Search</div>
    <div class="hero-title">Style<span>Finder</span></div>
    <div class="hero-subtitle">
        Upload any clothing image and discover the best matching products across Amazon,
        Flipkart, Myntra & more — instantly.
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Helper Functions ──────────────────────────────────────────────────────────
def safe_text(value, default=""):
    if value is None:
        return default
    return html.escape(str(value), quote=True)


def get_source_badge_class(source: str) -> str:
    source = str(source or "").lower()

    if "amazon" in source:
        return "badge-amazon"
    if "flipkart" in source:
        return "badge-flipkart"
    if "myntra" in source:
        return "badge-myntra"
    if "meesho" in source:
        return "badge-meesho"
    if "nykaa" in source:
        return "badge-nykaa"
    if "ajio" in source:
        return "badge-ajio"

    return "badge-default"


def rank_products(products, cloth_data):
    query_words = cloth_data.get("search_query", "").lower().split()

    for product in products:
        score = 0
        title_words = (product.get("title") or "").lower().split()

        for word in query_words:
            if word in title_words:
                score += 1

        product["score"] = score

    return sorted(products, key=lambda x: x.get("score", 0), reverse=True)


def format_rating(rating):
    if rating in [None, "", "N/A"]:
        return "No rating"

    return str(rating)


def format_reviews(reviews):
    if reviews in [None, "", "N/A"]:
        return ""

    return f" · {reviews} reviews"


def analyze_cloth_gemini(image_bytes: bytes, mime_type: str = "image/jpeg"):
    try:
        import google.generativeai as genai_sdk

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            st.error("GEMINI_API_KEY not set in environment.")
            return None

        genai_sdk.configure(api_key=api_key)

        model = genai_sdk.GenerativeModel("gemini-2.5-flash")

        img_part = {
            "mime_type": mime_type,
            "data": image_bytes
        }

        prompt = """
You are a fashion product tagging system for an online shopping app.

Look ONLY at the visible clothing item in the image.

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
- clothing_type examples: t-shirt, shirt, hoodie, jeans, jacket, dress, kurti, saree, top.
- pattern examples: plain, striped, checked, floral, graphic print, waffle knit, unknown.
- gender examples: men, women, unisex, unknown.
- search_query must be short and shopping-friendly.
- search_query should target Indian shopping results.
- Do not add brand names unless clearly visible.
Example: "men red plain round neck t-shirt"
"""

        response = model.generate_content([prompt, img_part])

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        st.error(f"Cloth analysis error: {e}")
        return None


def search_products_serpapi(query: str, max_results: int = 12):
    serpapi_key = os.getenv("SERPAPI_KEY")

    if not serpapi_key:
        st.error("SERPAPI_KEY not set in environment.")
        return []

    params = {
        "engine": "google_shopping",
        "q": query,
        "gl": "in",
        "hl": "en",
        "location": "India",
        "direct_link": "true",
        "api_key": serpapi_key,
    }

    allowed_sources = [
        "amazon",
        "flipkart",
        "myntra",
        "meesho",
        "nykaa",
        "ajio",
        "tata",
        "clovia",
        "biba",
        "libas",
        "indya",
        "zudio",
        "pantaloons",
        "westside",
        "savanna",
        "snitch"
    ]

    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=15
        )

        data = response.json()

        if "error" in data:
            st.warning(f"Search API: {data['error']}")
            return []

        results = []

        for item in data.get("shopping_results", []):
            if len(results) >= max_results:
                break

            source = item.get("source", "Unknown")
            source_lower = source.lower()

            if not any(store in source_lower for store in allowed_sources):
                continue

            results.append({
                "title": item.get("title", "No title"),
                "price": item.get("price", "N/A"),
                "source": source,
                "image": item.get("thumbnail") or item.get("serpapi_thumbnail"),
                "link": item.get("product_link") or item.get("link"),
                "rating": item.get("rating", "N/A"),
                "reviews": item.get("reviews", "N/A"),
            })

        return results

    except Exception as e:
        st.error(f"Product search error: {e}")
        return []


# ─── Layout ────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([4, 9], gap="small")

with left_col:
    st.markdown("""
    <style>
    [data-testid="column"]:first-child {
        background: #0e0e16;
        border-right: 1px solid rgba(255,255,255,0.06);
        padding: 2rem 1.5rem !important;
        min-height: calc(100vh - 180px);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="panel-label">📸 Upload Clothing Image</div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        label="Drop image here",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )

    if uploaded:
        st.image(uploaded, use_container_width=True)

    search_btn = st.button("✦ Find Similar Products", use_container_width=True)

    analysis_placeholder = st.empty()


with right_col:
    st.markdown('<div style="padding: 2rem 1rem;">', unsafe_allow_html=True)

    results_placeholder = st.empty()

    if not uploaded and not st.session_state.ranked_products:
        empty_html = '''
        <div class="empty-state">
            <span class="empty-icon">👗</span>
            <div class="empty-title">No image uploaded yet</div>
            <div class="empty-sub">Upload a clothing photo on the left to discover matching products</div>
        </div>
        '''
        st.markdown(empty_html.replace("\n", ""), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─── Search Logic ──────────────────────────────────────────────────────────────
if search_btn and uploaded:
    image_bytes = uploaded.getvalue()
    mime_type = uploaded.type or "image/jpeg"

    with left_col:
        with st.spinner("Analyzing your clothing..."):
            cloth_data = analyze_cloth_gemini(image_bytes, mime_type)

    if cloth_data:
        st.session_state.cloth_data = cloth_data

        with right_col:
            with st.spinner("Searching across Indian fashion stores..."):
                products = search_products_serpapi(
                    cloth_data.get("search_query", ""),
                    max_results=12
                )

        ranked_products = rank_products(products, cloth_data)

        st.session_state.products = products
        st.session_state.ranked_products = ranked_products

elif search_btn and not uploaded:
    st.warning("Please upload a clothing image first.")


# ─── Display Analysis + Results ────────────────────────────────────────────────
if st.session_state.cloth_data:
    cloth_data = st.session_state.cloth_data

    clothing_type = safe_text(cloth_data.get("clothing_type", "–"))
    color = safe_text(cloth_data.get("color", "–"))
    pattern = safe_text(cloth_data.get("pattern", "–"))
    style = safe_text(cloth_data.get("style", "–"))
    gender = safe_text(cloth_data.get("gender", "–"))
    search_query = safe_text(cloth_data.get("search_query", ""))

    analysis_html = f'''
    <div class="analysis-card">
        <div class="analysis-title">✦ Analysis Results</div>

        <div class="tag-row">
            <span class="tag gold"><span class="tag-key">Type</span>{clothing_type}</span>
            <span class="tag gold"><span class="tag-key">Color</span>{color}</span>
        </div>

        <div class="tag-row">
            <span class="tag"><span class="tag-key">Pattern</span>{pattern}</span>
            <span class="tag"><span class="tag-key">Style</span>{style}</span>
            <span class="tag"><span class="tag-key">Gender</span>{gender}</span>
        </div>

        <div class="query-box">
            <p>Search Query</p>
            <span>"{search_query}"</span>
        </div>
    </div>
    '''

    with analysis_placeholder.container():
        st.markdown(analysis_html.replace("\n", ""), unsafe_allow_html=True)

    ranked = st.session_state.ranked_products

    with results_placeholder.container():
        results_header_html = f'''
        <div class="results-header">
            <div class="results-title">Similar Products Found</div>
            <div class="results-count">{len(ranked)} results · Ranked by relevance</div>
        </div>
        '''

        st.markdown(results_header_html.replace("\n", ""), unsafe_allow_html=True)

        if ranked:
            cols = st.columns(4, gap="small")

            for index, product in enumerate(ranked):
                col = cols[index % 4]

                with col:
                    title = safe_text(product.get("title", "No title"))
                    price = safe_text(product.get("price", "N/A"))
                    source = safe_text(product.get("source", "Unknown"))
                    image_url = product.get("image")
                    link = product.get("link") or "#"
                    link = html.escape(str(link), quote=True)

                    badge_class = get_source_badge_class(product.get("source", "Unknown"))
                    score = product.get("score", 0)
                    rating = safe_text(format_rating(product.get("rating")))
                    reviews = safe_text(format_reviews(product.get("reviews")))

                    if image_url:
                        image_url = html.escape(str(image_url), quote=True)
                        img_html = f'<img src="{image_url}" alt="{title}" loading="lazy" />'
                    else:
                        img_html = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:3rem;opacity:0.3;">👗</div>'

                    card_html = f'''
                    <div class="product-card">
                        <div class="card-image-wrap">
                            {img_html}
                            <span class="source-badge {badge_class}">{source}</span>
                            <span class="score-badge">{score}</span>
                        </div>

                        <div class="card-body">
                            <div class="card-title">{title}</div>
                            <div class="card-price">{price}</div>
                            <div class="card-rating">⭐ {rating}{reviews}</div>
                            <a class="card-btn" href="{link}" target="_blank" rel="noopener noreferrer">Shop Now →</a>
                        </div>
                    </div>
                    '''

                    st.markdown(card_html.replace("\n", ""), unsafe_allow_html=True)

        else:
            no_results_html = '''
            <div class="empty-state">
                <span class="empty-icon">🔍</span>
                <div class="empty-title">No Indian store results found</div>
                <div class="empty-sub">Try a clearer image or another clothing item</div>
            </div>
            '''

            st.markdown(no_results_html.replace("\n", ""), unsafe_allow_html=True)