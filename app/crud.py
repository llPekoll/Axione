import csv

import requests
import unidecode
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models import Ville
from app.schema import DataIn


def get_right_town(db: Session, data: DataIn):
    """ Will select the best town in the right order """
    m2_max = int(data.loyer_max / data.surface)
    filters = (Ville.loyer < m2_max, Ville.departement == data.departement)
    villes = db.query(Ville).filter(*filters).order_by(Ville.note.desc())
    return villes[:10]


def init_db(db: Session):
    """ DB init """
    with open("/app/src/indicateurs-loyers-appartements.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        rows = []
        csvreader = list(csvreader)
        for row in csvreader:
            rows.append(row)
            try:
                ret = requests.get(
                    f"https://geo.api.gouv.fr/communes/{row[1]}?fields=nom,code,codesPostaux,codeDepartement,population&format=json"
                ).json()
            except Exception as e:
                print(f"INSEE code fail > {row[1]} >> Next")
                continue

            ville = ret.get("nom")
            ville = unidecode.unidecode(ville).lower()
            slug = f"{ville}-{row[1]}"
            req = requests.get(f"https://www.bien-dans-ma-ville.fr/{slug}/")
            note = None
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, "html.parser")
                note = soup.find("div", {"class": "total"})
                if note:
                    note = note.get_text()[:3]
                    note = note
            if not note:
                print("No Note")
                continue
            try:
                ville = Ville(
                    INSEE_code=row[1],
                    nom=ret.get("nom"),
                    loyer=float(row[7].replace(",", ".")),
                    note=note,
                    code_postal=ret.get("codesPostaux")[0],
                    population=ret.get("population"),
                    departement=ret.get("codeDepartement"),
                )
                db.add(ville)
                db.commit()
                print(f"just added {ret.get('nom')}")
            except Exception as e:
                print(f"Exception > {e}")
    return {"success": True}
