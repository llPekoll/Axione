from pydantic import BaseModel


class DataIn(BaseModel):
    departement: str
    surface: int
    loyer_max: int

    class Config:
        orm_mode = True


class Ville(BaseModel):
    note: float
    loyer: float
    nom: str
    code_postal: int
    population: int

    class Config:
        orm_mode = True
