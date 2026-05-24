from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite 檔案存在 backend/ 同層目錄
DATABASE_URL = "sqlite:///./texpress.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 需要此設定
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI Depends 用的 DB session 產生器"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
