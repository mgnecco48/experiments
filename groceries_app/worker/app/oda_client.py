import time
from typing import Iterator, Dict, Any, List, Union
import requests

BASE = "https://oda.com/api/v1/section-listing/categories"


def scrape_category(
    category_id: int, cursor: Union[int, str], size: int = 100
) -> Dict[str, Any]:
    url = f"{BASE}/{category_id}/{category_id}/"
    params = {
        "cursor": cursor,
        "sort": "default",
        "filters": "",
        "size": size,
    }
    headers = {
        "User-Agent": "groceries-bot/0.1 (learning project; contact: mgnecco48@gmail.com)"
    }
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_products(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = []
    num = 1

    # Finding the category name
    cat = api_response.get("title")

    for item in api_response.get("items", []):
        if item.get("type") != "product":
            continue
        a = item.get("attributes", {})
        # print(f"Item {num}-> \n{a}")
        num += 1

        # Finding out wether the product is discounted
        discount = a.get("discount")
        promotion = a.get("promotion")
        promotions = a.get("promotions") or []

        is_offer = bool(
            (discount and discount.get("is_discounted"))
            or promotion is not None
            or len(promotions) > 0
        )

        # creating the document to insert into Mongo
        out.append(
            {
                "category": cat,
                "source": "oda",
                "source_product_id": a.get("id"),
                "name": f"{a.get('name')}, {a.get('name_extra')}",
                "brand": a.get("brand"),
                "package_size": a.get("name_extra"),
                "price": float(a.get("gross_price")) if a.get("gross_price") else None,
                "unit_price": float(a.get("gross_unit_price"))
                if a.get("gross_unit_price")
                else None,
                "unit_price_qt": a.get("unit_price_quantity_abbreviation"),
                "currency": a.get("currency"),
                "origin": a.get("productionCountry")
                if a.get("productionCountry")
                else None,
                "is_available": (a.get("availability") or {}).get("is_available", None),
                "is_offer": is_offer,
                "offer_label": (promotion or {}).get("title")
                if promotion
                else (discount or {}).get("description_short"),
                "product_url": a.get("front_url"),
            }
        )
        # print(f"inserting in Mongo> {out}")
    return out


def iter_category_products(
    category_id, size: int = 50, sleep_time: float = 0.6
) -> Iterator[Dict[str, Any]]:
    cursor: Union[int, str] = 1

    while True:
        scraped_data = scrape_category(category_id, cursor=cursor, size=size)
        batch = extract_products(scraped_data)

        for p in batch:
            yield p

        has_more = scraped_data.get("has_more", False)
        next_cursor = scraped_data.get("next_cursor")

        if not has_more or not next_cursor:
            break

        cursor = next_cursor
        time.sleep(sleep_time)


categoriesOda = [
    21,
    391,
    1029,
    22,
    24,
    9,
    57,
    23,
    1136,
    1210,
    3234,
    6,
    393,
    1137,
    1138,
    4,
    116,
    1213,
    1268,
    1099,
    1100,
    49,
    487,
    53,
    50,
    52,
    51,
    142,
    148,
    2872,
    2874,
    2875,
    2876,
    2877,
    28,
    389,
    388,
    390,
    204,
    304,
    307,
    310,
    29,
    3352,
    3409,
    3399,
    289,
    301,
    292,
    1090,
    3414,
    3382,
    1351,
    1350,
    1484,
    3379,
    45,
    235,
    122,
    47,
    97,
    46,
    44,
    1101,
    2640,
    1140,
    1264,
    33,
    1116,
    410,
    96,
    1113,
    11,
    313,
    1269,
    113,
    448,
    1277,
    38,
    3267,
    1280,
    1245,
    1237,
    1243,
    1244,
    1236,
    345,
    359,
    65,
    61,
    63,
    66,
    12,
    3079,
    1247,
    406,
    1045,
    1180,
    1214,
    1219,
    1131,
    19,
    1229,
    1232,
    18,
    56,
    409,
    10,
    2846,
    110,
    391,
    423,
    2832,
    68,
    69,
    70,
    71,
    100,
    2780,
    443,
    137,
    74,
    1198,
    562,
    78,
    475,
    394,
    2910,
    367,
    1316,
    400,
    372,
    3264,
    1183,
    1185,
    434,
    374,
    1188,
    376,
    481,
    476,
    1057,
    3239,
    93,
    88,
    172,
    385,
    181,
    441,
    334,
    1064,
    1096,
    178,
    3060,
    104,
    90,
    402,
    403,
    1027,
    404,
    131,
    134,
    328,
    386,
    2842,
    2843,
    2844,
    2845,
    103,
    364,
    382,
    363,
    489,
    498,
    492,
    499,
    490,
    491,
    495,
    494,
    493,
    497,
    502,
    3250,
    3251,
    3253,
    3252,
    3343,
    2578,
    3115,
    2579,
    3323,
    2576,
    2575,
    2572,
]


# Debuggin section
# print(f"Raw Response: {scrape_category(49, 1)}")
# print()
# print("Only products:")
# products = extract_products(scrape_category(22, 1))
#
# for i, product in enumerate(products):
#     print()
#     print(f"Product #{i}:")
#     for item in product.items():
#         print(item)
