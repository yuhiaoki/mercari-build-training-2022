import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# from io import BytesIO
# from typing import List,Dict
# import json
from collections import OrderedDict
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import hashlib
import shutil

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
def root(db: Session = Depends(get_db)):
    db.add(models.Category(name="food"))
    db.add(models.Category(name="book"))
    db.add(models.Category(name="fashon"))
    db.flush()
    db.add(
        models.Items(
            name="fish", category_id=1, image_filename="python\image\default.jpg"
        )
    )
    db.add(
        models.Items(
            name="dictionary",
            category_id=2,
            image_filename="python\image\default.jpg",
        )
    )
    db.add(
        models.Items(
            name="T-shirt", category_id=3, image_filename="python\image\default.jpg"
        )
    )
    db.add(
        models.Items(
            name="jaket", category_id=3, image_filename="python\image\default.jpg"
        )
    )
    db.flush()
    db.commit()
    return {"message": "Hello, world!"}


@app.post("/items")
async def add_item(
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # with open("items.json") as f:
    #     d = json.load(f, object_pairs_hook=OrderedDict)
    #     keys = ["name", "category"]
    #     values = [name, category]
    #     item = dict(zip(keys, values))
    #     d["items"].append(item)
    # with open("items.json", "w") as f:
    #     json.dump(d, f, indent=2, ensure_ascii=False)
    if not image.filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")
    category_model = models.Category()
    category_model.name = category
    db.add(category_model)
    db.flush()
    item_model = models.Items()
    item_model.name = name
    item_model.category_id = category_model.id
    sha256 = hashlib.sha256(image.file.read()).hexdigest() + ".jpg"
    item_model.image_filename = sha256
    path = images / sha256
    with open(path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    db.add(item_model)
    db.commit()
    return {"message": f"item received: {name}"}

    # with open("items.json") as f:
    #     d = json.load(f)
    # return d


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    item_model = (
        db.query(
            models.Items.id,
            models.Items.name,
            models.Items.image_filename,
            models.Category.name.label("category"),
        )
        .outerjoin(models.Category, models.Category.id == models.Items.category_id)
        .all()
    )
    if item_model is not None:
        return {"items": item_model}
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/items/{id}")
def get_item(id: str, db: Session = Depends(get_db)):
    item_model = db.query(models.Items).filter(models.Items.id == id).all()
    if item_model is not None:
        return {"items": item_model}
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/search")
def search_items(keyword: str, db: Session = Depends(get_db)):
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
