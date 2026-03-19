import time
import requests
from typing import Iterator, Dict, Any, List


BASE = "https://platform-rest-prod.ngdata.no/api/products/1300/7080001150488"
CATEGORIES_URL = "https://meny.no/api/categories"


def get_categories(url):
    response = requests.get(url)
    response.raise_for_status()
    categories = response.json()
    category_list = []
    for category in categories:
        category_list.append(category.get("categoryName"))

    return category_list


# Meny exposes the full catalog in one API endpoint, so with only one request I can get all products.
# Still need to work through the pagination.
def scrape_all_products(page: int, page_size: int = 100) -> Dict[str, Any]:
    params = {
        "page": page,
        "page_size": page_size,
        "full_response": "true",
        "fieldset": "maximal",
        "facets": "Category,Allergen",
        "showNotForSale": "true",
    }
    headers = {"User-Agent": "groceries-app/0.1 (learning project)"}
    response = requests.get(BASE, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_products(api_response: Dict[str, Any]):
    out = []

    for item in api_response.get("hits", {}).get("hits", []):
        if item.get("_type") != "product":
            continue

        a = item.get("_source", {})
        promotions = a.get("promotions", []) or []
        promo_text = [p.get("promoMarketTextLong") for p in promotions]

        out.append(
            {
                "category": a.get("categoryName"),
                "source": "meny",
                "source_product_id": item.get("_id"),
                "name": f"{a.get('title')}, {a.get('subtitle')}",
                "brand": a.get("brand"),
                "package_size": a.get("packageSize"),
                "price": float(a.get("pricePerUnitOriginal")),
                "unit_price": float(a.get("calcPricePerUnit"))
                if a.get("calcPricePerUnit")
                else None,
                "unit_price_qt": a.get("calcUnit"),
                "currency": "NOK",
                "origin": a.get("productionCountry"),
                "is_available": not a.get("isOutOfStock"),
                "is_offer": a.get("isOffer"),
                "offer_label": promo_text,
                "product_url": a.get("slugifiedUrl"),
            }
        )
    return out


def iter_all_products(page_size=200, sleep_time=0.6):
    page = 1

    while True:
        scraped_data = scrape_all_products(page, page_size)
        batch = extract_products(scraped_data)

        if not batch:
            break

        for p in batch:
            yield p

        if len(batch) < page_size:
            break

        page += 1
        time.sleep(sleep_time)


print("Only products:")
products = extract_products(scrape_all_products(1))

for i, product in enumerate(products):
    print()
    print(f"Product #{i + 1}:")
    for item in product.items():
        print(item)
