import os
from datetime import datetime, UTC
from pymongo import MongoClient
import oda_client
import meny_client
import time

SCRAPE_INTERVAL = 3600 * 4

# -----------------------
# Mongo Connection
# -----------------------

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client["groceries_db"]  # <-- choose your real DB name

products_col = db["products"]
price_history_col = db["price_history"]


# -----------------------
# Worker Logic
# -----------------------


def run_worker(source, category=None):
    count_total = 0
    count = 0
    if source == "ODA":
        print(f"\n-> scraping category {category}")

        try:
            for product in oda_client.iter_category_products(category):
                now = datetime.now(UTC)

                # Upsert latest product (just want to know the current price)
                products_col.update_one(
                    {
                        "product_key": f"{product['source']}_{product['source_product_id']}",
                        "source": product["source"],
                        "source_product_id": product["source_product_id"],
                    },
                    {
                        "$set": {
                            "category": product["category"],
                            "name": product["name"],
                            "brand": product["brand"],
                            "package_size": product["package_size"],
                            "price": product["price"],
                            "unit_price": product["unit_price"],
                            "unit_price_qt": product["unit_price_qt"],
                            "currency": product["currency"],
                            "origin": product["origin"],
                            "is_available": product["is_available"],
                            "is_offer": product["is_offer"],
                            "offer_label": product["offer_label"],
                            "product_url": product["product_url"],
                            "last_updated": now,
                        }
                    },
                    upsert=True,
                )

                # Insert into price history (in this one i insert every time to build a history)
                price_history_col.insert_one(
                    {
                        "source": product["source"],
                        "product_key": f"{product['source']}_{product['source_product_id']}",
                        "price": product["price"],
                        "is_offer": product["is_offer"],
                        "timestamp": now,
                    }
                )

                # Simple print for visibility
                print(
                    f"{product['source']} | "
                    f"{product['category']} | "
                    f"[{now.isoformat()}] "
                    f"{product['name']} | "
                    f"{product['brand']} | "
                    f"{product['price']} NOK"
                )

                count += 1
                count_total += 1

        except Exception as e:
            print(f"Category {category} failed: {e}")

        print(f"Category {category} finished. Total products: {count}")
        count = 0

    elif source == "MENY":
        try:
            for product in meny_client.iter_all_products():
                count += 1
                now = datetime.now(UTC)

                # Upsert latest product (just want to know the current price)
                products_col.update_one(
                    {
                        "product_key": f"{product['source']}_{product['source_product_id']}",
                        "source": product["source"],
                        "source_product_id": product["source_product_id"],
                    },
                    {
                        "$set": {
                            "category": product["category"],
                            "name": product["name"],
                            "brand": product["brand"],
                            "package_size": product["package_size"],
                            "price": product["price"],
                            "unit_price": product["unit_price"],
                            "unit_price_qt": product["unit_price_qt"],
                            "currency": product["currency"],
                            "origin": product["origin"],
                            "is_available": product["is_available"],
                            "is_offer": product["is_offer"],
                            "offer_label": product["offer_label"],
                            "product_url": product["product_url"],
                            "last_updated": now,
                        }
                    },
                    upsert=True,
                )

                # Insert into price history (in this one i insert every time to build a history)
                price_history_col.insert_one(
                    {
                        "source": product["source"],
                        "product_key": f"{product['source']}_{product['source_product_id']}",
                        "price": product["price"],
                        "is_offer": product["is_offer"],
                        "timestamp": now,
                    }
                )

                # Simple print for visibility
                print(
                    f"{product['source']} | "
                    f"{product['category']} | "
                    f"[{now.isoformat()}] "
                    f"{product['name']} | "
                    f"{product['brand']} | "
                    f"{product['price']} NOK"
                )

        except Exception as e:
            print(f"Error: {e}")

        print(f"Catalog finished. Total products: {count}")

    return count_total


def main():

    sources = ["ODA", "MENY"]

    while True:
        print("\n=== Starting full scrape cycle ===")

        for source in sources:
            if source == "ODA":
                print(f"\n=== Inserting Products for {source} ===")
                for category in oda_client.categoriesOda:
                    run_worker(source, category)
            elif source == "MENY":
                print(f"\n=== Inserting Products for {source} ===")
                run_worker(source)
            else:
                print("Invalid Source")
                break

        print(f"=== Scrape cycle finished. Sleeping {SCRAPE_INTERVAL / 3600}hrs ===")
        time.sleep(SCRAPE_INTERVAL)


if __name__ == "__main__":
    main()
