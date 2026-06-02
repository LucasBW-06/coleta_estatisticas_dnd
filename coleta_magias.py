import requests
import json
import re
from sqlalchemy import create_engine, select, MetaData, insert, text

username = "root"
password = "admin"
host = "localhost"
port = 3306
database = "estatisticas_dnd"

connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string, echo=False)

metadata = MetaData()

metadata.reflect(bind=engine)

magias_tabela = metadata.tables["magias"]

escolas_aux = {
    "A": "Abjuration",
    "C": "Conjuration",
    "D": "Divination",
    "E": "Enchantment",
    "V": "Evocation",
    "I": "Illusion",
    "N": "Necromancy",
    "T": "Transmutation"
}

def get_or_create(valor, tabela, coluna):
    if valor is None:
        return None

    if isinstance(tabela, str):
        tabela = metadata.tables[tabela]

    with engine.begin() as conn:

        result = conn.execute(
            select(tabela.c.id).where(tabela.c[coluna] == valor)
        ).first()

        if result:
            return result[0]

        result = conn.execute(
            insert(tabela).values({coluna: valor})
        )

        return result.inserted_primary_key[0]

def average_damage(formula):
    total = 0

    for qtd, faces in re.findall(r'(\d+)d(\d+)', formula):
        total += int(qtd) * ((int(faces) + 1) / 2)

    for bonus in re.findall(r'(?<!d)([+-]\s*\d+)', formula):
        total += int(bonus.replace(" ", ""))

    return total

url = "https://5e.tools/data/spells/spells-phb.json"
response = requests.get(url)
data = response.json()
magias = data["spell"]
for magia in magias:
    for i in magia:
        print(f"{i}: {magia[i]}")
    dados = {}
    dados["nome"] = magia.get("name")
    dados["nivel"] = str(magia.get("level"))
    
    escola = magia.get("school")
    if escola:
        dados["escola_id"] = get_or_create(escolas_aux[escola], "escolas", "escola")
    
    magia_id = ""
    with engine.begin() as conn:
        result = conn.execute(
            insert(magias_tabela),
            dados
        )
        magia_id = result.inserted_primary_key[0]

        conn.commit()
        conn.close()
    
    with engine.begin() as conn:
        entradas = magia.get("entries")
        for trecho in entradas:
            texto = ''
            if isinstance(trecho, str):
                texto = trecho
            else:
                if trecho.get("entries"):
                    texto = trecho.get("entries")[0]
                
            matches = re.findall(r'\{@damage ([^}]+)\}\s+([a-z,\s]+?(?:\s+or\s+[a-z]+|\s+and\s+[a-z]+)*)\s+damage',
                texto)
            for m in matches:
                media = 0
                if m[0]:
                    media = average_damage(m[0])
                tipos = re.split(r'\s*,\s*or\s+|\s+or\s+|\s+and\s+|,\s*', m[1])
                tipos = [t for t in tipos if t]
                for tipo in tipos:
                    if len(tipo.split()) == 1:
                        dano_id = get_or_create(tipo, "danos", "dano")
                        conn.execute(
                            insert(metadata.tables["dano_magia"]).values({"dano_id": dano_id, "magia_id": magia_id, "media": media})
                        )

        conn.commit()
        conn.close()