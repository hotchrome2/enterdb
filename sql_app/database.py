from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
そもそもなぜSQLAlchemy を使うかというと、
SQLAlchemy を使用すると、DBのデータをPythonオブジェクトとみなして扱うことができるから。
"""


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# オブジェクトの情報はセッションを通じてDBに反映される。
# DBクエリの実行はセッションを通じて行う。
# SessionLocalはセッションを作るためのクラス。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base()はクラスBaseを返す。
# Baseから派生クラス（モデル）を作成すると作成段階でテーブル定義に紐づく（SQLAlchemy の特殊な機能）
# Pythonのメタクラスを活用している（クラス定義が発生したら何かをする）
Base = declarative_base()

# 実際のテーブル作成契機は、main.pyの Base.metadata.create_all(bind=engine)
