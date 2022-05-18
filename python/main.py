import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


# from typing import List,Dict
import json
from collections import OrderedDict

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello, world!"}


@app.post("/items")
def add_item(
    name: str = Form(...), category: str = Form(...), db: Session = Depends(get_db)
):
    # with open("items.json") as f:
    #     d = json.load(f, object_pairs_hook=OrderedDict)
    #     keys = ["name", "category"]
    #     values = [name, category]
    #     item = dict(zip(keys, values))
    #     d["items"].append(item)
    # with open("items.json", "w") as f:
    #     json.dump(d, f, indent=2, ensure_ascii=False)
    item_model = models.Items()
    item_model.name = name
    item_model.category = category

    db.add(item_model, item_model)
    db.commit()
    return {"message": f"item received: {name}"}

    # with open("items.json") as f:
    #     d = json.load(f)
    # return d


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    if db.query(models.Items).all() is not None:
        return {"items": db.query(models.Items).all()}
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/search")
def serch_items(keyword: str, db: Session = Depends(get_db)):
    item_model = db.query(models.Items).filter(models.Items.name == keyword).all()
    if item_model is not None:
        return {"items": item_model}
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image

    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
