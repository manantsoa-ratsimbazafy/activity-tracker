from app.db import Base, engine
from app.models import Activity, TimeEntry # importé pour enregistrer le modèle auprès de Base


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    