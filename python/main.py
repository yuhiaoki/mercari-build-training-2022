import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import hashlib
import shutil
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base, SessionLocal
from sqlalchemy_utils import UUIDType
import uuid

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
Base.metadata.create_all(bind=engine)


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # children = relationship("items")


class Items(Base):
    __tablename__ = "items"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    category_id = Column(
        Integer,
        ForeignKey(
            "category.id",
        ),
    )
    image_filename = Column(String)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def root(db: Session = Depends(get_db)):
    db.add(Category(name="food"))
    db.add(Category(name="book"))
    db.add(Category(name="fashon"))
    db.flush()
    db.add(Items(name="fish", category_id=1, image_filename="python\image\default.jpg"))
    db.add(
        Items(
            name="dictionary",
            category_id=2,
            image_filename="python\image\default.jpg",
        )
    )
    db.add(
        Items(name="T-shirt", category_id=3, image_filename="python\image\default.jpg")
    )
    db.add(
        Items(name="jaket", category_id=3, image_filename="python\image\default.jpg")
    )
    db.flush()
    db.commit()
    return {"message": "Hello, world!"}


@app.post("/items")
async def add_item(
    # data: Data,
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not image.filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")
    category_model = Category()
    category_model.name = category
    db.add(category_model)
    db.flush()
    item_model = Items()
    item_model.name = name
    item_model.category_id = category_model.id
    sha256 = hashlib.sha256(image.filename.encode()).hexdigest() + ".jpg"
    item_model.image_filename = sha256
    path = images / sha256
    with open(path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    db.add(item_model)
    db.commit()
    return {"message": f"item received: {name}"}


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    item_model = (
        db.query(
            Items.id,
            Items.name,
            Items.image_filename,
            Category.name.label("category"),
        )
        .outerjoin(Category, Category.id == Items.category_id)
        .all()
    )
    if item_model is not None:
        return item_model
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/items/{id}")
def get_item(id: str, db: Session = Depends(get_db)):
    item_model = db.query(Items).filter(Items.id == id).all()
    if item_model is not None:
        return {"items": item_model}
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/search")
def search_items(keyword: str, db: Session = Depends(get_db)):
    item_model = db.query(Items).filter(Items.name == keyword).all()
    if item_model is not None:
        return {"items": item_model}
    raise HTTPException(status_code=404, detail="item not found")


@app.get("/image/{items_id}")
async def get_image(items_id, db: Session = Depends(get_db)):
    # Create image path
    id = os.path.splitext(items_id)[0]
    items_model = db.query(Items).filter(Items.id == id).first()
    image = images / items_model.image_filename

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"
    print(image)
    return FileResponse(image)


@app.delete("/del")
def delete(db: Session = Depends(get_db)):
    db.query(Items).delete()
    db.query(Category).delete()
    db.commit()
    return {"msg": "delete"}
