import requests
import json
from sqlalchemy import create_engine, select, MetaData, insert, update

username = "root"
password = "admin"
host = "localhost"
port = 3306
database = "estatisticas_dnd"

connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

metadata = MetaData()

metadata.reflect(bind=engine)

monstros = metadata.tables["monstros"]

abv = {}
with open("abv.json", "r", encoding="utf-8") as f:
    abv = json.load(f)

tamanhos = {
    "T": "Tiny",
    "S": "Small",
    "M": "Medium",
    "L": "Large",
    "H": "Huge",
    "G": "Gargantuan"
}

def get_or_create(valor, tabela, coluna):
    if valor is None:
        return None

    with engine.begin() as conn:
        
        result = conn.execute(
            select(tabela.c.id).where(getattr(tabela.c, coluna) == valor)
        ).first()

        if result:
            return result[0]

        result = conn.execute(
            insert(tabela).values({coluna: valor})
        )

        return result.inserted_primary_key[0]

for key in abv:
    url = f"https://5e.tools/data/bestiary/bestiary-{key.lower()}.json"
    response = requests.get(url)
    if response.status_code != 404:
        data = response.json()
        monstros = data["monster"]
        for monstro in monstros:
            dados = {}
            dados["nome"] = monstro.get("name")
            dados["forca"] = monstro.get("str")
            dados["destreza"] = monstro.get("dex")
            dados["constituicao"] = monstro.get("con")
            dados["inteligencia"] = monstro.get("int")
            dados["sabedoria"] = monstro.get("wis")
            dados["carisma"] = monstro.get("cha")

            ca = monstro.get("ac")
            if isinstance(ca[0], int):
                dados["classe_armadura"] = ca[0]
            else:
                dados["classe_armadura"] = ca[0].get("ac")

            dados["pontos_vida"] = monstro.get("hp").get("avarage")

            nd = monstro.get("cr")
            if isinstance(nd, str):
                dados["nivel_desafio"] = nd
            else:
                dados["nivel_desafio"] = nd.get("cr")

            dados["fonte"] = abv["key"]