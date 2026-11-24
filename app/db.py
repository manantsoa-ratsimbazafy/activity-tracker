import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

db_pwd_file = Path(__file__).resolve().parent.parent / "secrets" / "db_password.txt"

if not db_pwd_file.is_file():
    raise FileNotFoundError(
        f"The password file ({db_pwd_file}) is missing or is stored at a wrong location. Make sure the file is located at secrets/db_password.txt."
    )

password = db_pwd_file.read_text(encoding="utf-8").strip()
if not password:
    raise ValueError("The password file is empty")


def build_url(env_db_name: str = "DATABASE_NAME"):
    db_name = (os.getenv(env_db_name) or "").strip()
    if not db_name:
        raise ValueError(f"{env_db_name} in the .env file is missing or has no value")

    db_host = (os.getenv("DATABASE_HOST") or "").strip()
    if not db_host:
        raise ValueError("DATABASE_HOST in the .env file is missing or has no value")

    db_user = (os.getenv("DATABASE_USER") or "").strip()
    if not db_user:
        raise ValueError("DATABASE_USER in the .env file is missing or has no value")

    return URL.create(
        drivername="postgresql+psycopg",
        username=db_user,
        password=password,
        host=db_host,
        database=db_name,
    )


db_url = build_url("DATABASE_NAME")

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
