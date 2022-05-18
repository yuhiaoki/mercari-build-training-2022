# -*- coding:utf-8 -*-
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy import Column, Integer, String

from sqlalchemy_utils import UUIDType

import uuid

Base = sqlalchemy.ext.declarative.declarative_base()


class Items(Base):
    __tablename__ = "items"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    category = Column(String)

    @staticmethod
    def add_column(engine, column):
        column_name = column.compile(dialect=engine.dialect)
        column_type = column.type.compile(engine.dialect)
        engine.execute(
            "ALTER TABLE %s ADD COLUMN %s %s"
            % (Items.__tablename__, column_name, column_type)
        )


def main():
    url = "sqlite:///../db/mercari.sqlite3"

    engine = sqlalchemy.create_engine(url, echo=True)

    # テーブルをドロップ
    Base.metadata.drop_all(engine)

    # テーブルを作成
    Base.metadata.create_all(engine)

    # テーブルにカラムを追加
    column = sqlalchemy.Column("image_filename", String)
    Items.add_column(engine, column)


if __name__ == "__main__":
    main()
