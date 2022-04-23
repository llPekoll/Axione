import csv
from typing import List

from fastapi import Depends, FastAPI

from app.crud import get_right_town, init_db
from app.database import SessionLocal, engine
from app.models import Base
from app.schema import DataIn, Ville

Base.metadata.create_all(bind=engine)

app = FastAPI()


def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# print("========= INIT DB ===========")
# init_db()
# print("========= DB INITILAZED! ===========")
# print("========= you now can send request ===========")


@app.get("/townfinder", response_model=List[Ville])
def save_device_info(data: DataIn, db=Depends(db)):
    """ town finder endpoint """
    return get_right_town(db, data)


@app.get("/init")
def save_device_info(db=Depends(db)):
    """ DB init endpoint """
    return init_db(db)
