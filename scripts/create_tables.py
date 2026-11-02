from app.db import Base, engine
from app.models import Activity, TimeEntry # imported to register the models with Base


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    