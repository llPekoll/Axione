from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Ville(Base):
    __tablename__ = "villes"

    id = Column(Integer, primary_key=True, index=True)
    INSEE_code = Column(Integer)
    nom = Column(String)
    loyer = Column(Float)
    note = Column(Float)
    code_postal = Column(Integer)
    population = Column(Integer)
    departement = Column(Integer)
