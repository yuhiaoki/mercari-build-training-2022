from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy_utils import UUIDType

import uuid


class Items(Base):
    __tablename__ = "items"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    category = Column(String)
