from dotenv import load_dotenv
from cloth_analyzer import analyze_cloth
from product_search import search_products

load_dotenv()


def rank_products(products, cloth_data):
    query_words = cloth_data["search_query"].lower().split()

    ranked_products = []

    for product in products:
        title = product["title"] or ""
        title_words = title.lower().split()

        for word in query_words:
            if word in title_words:
                score += 1

        product["score"] = score
        ranked_products.append(product)

    ranked_products.sort(key=lambda x: x["score"], reverse=True)

    return ranked_products


def display_cloth_analysis(cloth_data):
    print("\n===== CLOTH ANALYSIS =====")
    print("Clothing Type:", cloth_data.get("clothing_type"))
    print("Color:", cloth_data.get("color"))
    print("Pattern:", cloth_data.get("pattern"))
    print("Style:", cloth_data.get("style"))
    print("Gender:", cloth_data.get("gender"))
    print("Search Query:", cloth_data.get("search_query"))


def display_products(products):
    print("\n===== BEST PRODUCT MATCHES =====")

    if not products:
        print("No products found.")
        return

    for i, product in enumerate(products, start=1):
        print(f"\nProduct {i}")
        print("Title:", product.get("title"))
        print("Price:", product.get("price"))
        print("Source:", product.get("source"))
        print("Match Score:", product.get("score"))
        print("Link:", product.get("link"))


def main():
    print("===== AI CLOTH FINDER =====")

    image_path = input("Enter clothing image path: ")

    print("\nAnalyzing cloth image...")
    cloth_data = analyze_cloth(image_path)

    if not cloth_data:
        print("Could not analyze cloth image.")
        return

    display_cloth_analysis(cloth_data)

    print("\nSearching similar products...")
    products = search_products(cloth_data["search_query"])

    ranked_products = rank_products(products, cloth_data)

    display_products(ranked_products)


if __name__ == "__main__":
    main()