from fastapi import FastAPI
import os
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel

class ProductCreate(BaseModel):
                    name : str
                    store :str
                    category : str

app = FastAPI()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client[os.getenv("DATABASE_NAME")]


@app.get("/")
def root():
    return {"message": "Grocery API running"}

@app.post("/products")
def create_product(product: ProductCreate):

    product_doc = {
        "name": product.name,
        "store": product.store,
        "category": product.category,
        "created_at": datetime.utcnow()
    }

    result = db.products.update_one({
            "name": product.name,
            "store": product.store
        },
        {"$setOnInsert": product_doc},
        upsert=True
    )

    return {"message": "Product created or already exists",
    }


@app.post("/dummy/price")
def create_dummy_price():
    price_doc = {
        "product_name": "Tine Lettmelk 1L",
        "store": "Kiwi",
        "price": 19.90,
        "is_offer": False,
        "timestamp": datetime.now()
    }

    db.price_history.insert_one(price_doc)

    return {"message": "Price history inserted"}
