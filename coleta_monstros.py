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

alinhamentos = {
    "A": "Any",
    "U": "Unaligned",
    "N": "Neutral",
    "C": "Chaotic",
    "L": "Lawful",
    "G": "Good",
    "E": "Evil"
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
            
            type = monstro.get("type")
            
            if isinstance(type, str):
                dados["tipo"] = type
            else:
                tipo = type.get("type")
                subtipo = type.get("tags")
                if isinstance(subtipo, list):
                    subtipo = subtipo[0]
                else:
                    subtipo = subtipo.get("tag")
                
                if tipo == "swarm":
                    temp = subtipo
                    subtipo = tipo
                    tipo = temp
                    
                dados["tipo"] = get_or_create(tipo, "tipo", "tipo")
                dados["subtipo"] = get_or_create(subtipo, "subtipo", "subtipo")
                
            alinhamento = monstro.get("alignment")
            
            monstro_id = ""
            with engine.begin() as conn:
                result = conn.execute(
                    insert(monstros),
                    dados
                )
                monstros_id = result.inserted_primary_key[0]
                
                conn.commit()
                conn.close()
            
            
            with engine.begin() as conn:
                deslocamento = monstro.get("speed")
                for i in deslocamento:
                    dis = ''
                    if isinstance(deslocamento[i], int):
                        dis = deslocamento[i]
                    else:
                        dis = deslocamento[i]["number"]
                    
                    dis = dis/5
                    
                    des = get_or_create(i, "deslocamento", "deslocamento")
                    
                    conn.execute(
                        insert("deslocamento_monstro").values({"deslocamento_id": des, "monstro_id": monstro_id, "distancia": dis})
                    )
                    
                
                