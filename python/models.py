from sqlalchemy import Column, Integer, String
from database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
