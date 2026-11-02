import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()
db_url = os.getenv("DATABASE_URL")

if db_url is None:
    raise RuntimeError("DATABASE_URL is missing in the .env file")

engine = create_engine(db_url)

SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(result.scalar())  # 1
        # print(result.fetchone()) # (1,)
