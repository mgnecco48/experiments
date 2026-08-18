from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


product_list = [
    {
        "item_name": "Salsa Verde",
        "spice_level": "No pica",
        "size": 270,
        "image_url": "http://127.0.0.1:8000/media/SalsaVerde.png",
        "price": 250,
    },
    {
        "item_name": "Salsa Roja",
        "spice_level": "Pica mas o menos",
        "size": 270,
        "image_url": "http://127.0.0.1:8000/media/SalsaRoja.png",
        "price": 250,
    },
    {
        "item_name": "Salsa Macha",
        "spice_level": "Pica mucho",
        "size": 270,
        "image_url": "http://127.0.0.1:8000/media/SalsaMacha.png",
        "price": 250,
    },
    {
        "item_name": "Salsa Habanero",
        "spice_level": "Pica muchisimo",
        "size": 270,
        "image_url": "http://127.0.0.1:8000/media/SalsaHabanero.png",
        "price": 250,
    },
]

tacos = []


class Salsa(BaseModel):
    item_name: str
    spice_level: str
    size: float | None = None
    desc: str | None = None
    image_url: str
    price: float


class Taco(BaseModel):
    name: str = Field(default="", title="El nombre del taco", max_length=25)
    protein: str
    salsa: Salsa


app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Application": "Salsas Backend"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": (item_id * 2), "q": q}


@app.get("/salsas/")
async def get_salsas(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return product_list[skip : skip + limit]


@app.get("/tacos/")
async def get_tacos(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return tacos[skip : skip + limit]


@app.post("/salsas/")
async def create_salsa(salsa: Salsa):
    product_list.append(salsa.model_dump())
    return salsa


@app.post("/tacos/")
async def create_taco(taco: Taco):
    tacos.append(
        {
            "name": taco.name,
            "protein": taco.protein,
            "salsa": f"Recommended with {taco.salsa.item_name}",
        }
    )
    return taco
