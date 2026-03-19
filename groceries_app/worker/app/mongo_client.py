from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client["grocery_db"]

products_col = db["products"]
price_history_col = db["price_history"]
