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
