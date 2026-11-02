from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os


load_dotenv()
db_url = os.getenv("DATABASE_URL")

if db_url is None:
    raise RuntimeError("Il manque une variable DATABASE_URL dans le fichier .env")
engine = create_engine(db_url)

SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

class Base(DeclarativeBase):
    pass


if __name__ == "__main__":
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(result.scalar()) # 1
        # print(result.fetchone()) # (1,)