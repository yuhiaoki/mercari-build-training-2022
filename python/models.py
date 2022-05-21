import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
from sqlalchemy_utils import UUIDType
import uuid


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


# def main():
#     url = "sqlite:///mercari.sqlite3"
#     engine = sqlalchemy.create_engine(url, echo=True)
#     # # テーブルをドロップ
#     Base.metadata.drop_all(engine)
#     # テーブルを作成
#     Base.metadata.create_all(engine)

#     session = SessionLocal()

# テーブルにカラムを追加
# column = sqlalchemy.Column("image_filename", String, primary_key=False)
# Items.add_column(engine, column)
