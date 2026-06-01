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

monstros_tabela = metadata.tables["monstros"]

abv = {}
with open("abv.json", "r", encoding="utf-8") as f:
    abv = json.load(f)

tamanhos_aux = {
    "T": "Tiny",
    "S": "Small",
    "M": "Medium",
    "L": "Large",
    "H": "Huge",
    "G": "Gargantuan"
}

alinhamentos_aux = {
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

def bring_alignment(alinhamento):
    if len(alinhamento) > 1:
        return None
    aux = []
    for i in alinhamento:
        aux.append(alinhamentos_aux[i])
    return " ".join(aux)

for key in abv:
    url = f"https://5e.tools/data/bestiary/bestiary-{key.lower()}.json"
    response = requests.get(url)
    if response.status_code != 404:
        data = response.json()
        monstros = data["monster"]
        for monstro in monstros:
            for i in monstro:
                print(f"{i}: {monstro[i]}")
            
            print("")
            dados = {}
            dados["nome"] = monstro.get("name")
            dados["forca"] = monstro.get("str")
            dados["destreza"] = monstro.get("dex")
            dados["constituicao"] = monstro.get("con")
            dados["inteligencia"] = monstro.get("int")
            dados["sabedoria"] = monstro.get("wis")
            dados["carisma"] = monstro.get("cha")

            ca = monstro.get("ac")
            if ca:
                if isinstance(ca[0], int):
                    dados["classe_armadura"] = ca[0]
                else:
                    dados["classe_armadura"] = ca[0].get("ac")
            
            pv = monstro.get("hp")
            if pv:
                dados["pontos_vida"] = pv.get("average")

            nd = monstro.get("cr")
            if nd:
                if isinstance(nd, str):
                    dados["nivel_desafio"] = nd
                else:
                    dados["nivel_desafio"] = nd.get("cr")

            dados["fonte"] = abv[key]
            
            tipo_c = monstro.get("type")
            
            tamanhos = None
            if tipo_c:
                if isinstance(tipo_c, str):
                    dados["tipo_id"] = get_or_create(tipo_c, "tipos", "tipo")
                else:
                    tipo = tipo_c.get("type")
                    subtipo = tipo_c.get("tags")
                    swarmSize = tipo_c.get("swarmSize")
                    if swarmSize:
                        subtipo = "swarm"
                        tamanhos = swarmSize

                    if not isinstance(tipo, dict):
                        if isinstance(subtipo, list):
                            subtipo = subtipo[0]
                        elif isinstance(subtipo, dict):
                            subtipo = subtipo.get("tags")

                        if isinstance(subtipo, dict):
                                subtipo = subtipo.get("tag")

                        if tipo == "swarm":
                            temp = subtipo
                            subtipo = tipo
                            tipo = temp
                        
                        dados["tipo_id"] = get_or_create(tipo, "tipos", "tipo")
                        dados["subtipo_id"] = get_or_create(subtipo, "subtipos", "subtipo")
            
            monstro_id = ""
            with engine.begin() as conn:
                print("")
                result = conn.execute(
                    insert(monstros_tabela),
                    dados
                )
                monstro_id = result.inserted_primary_key[0]

                conn.commit()
                conn.close()

            with engine.begin() as conn:
                deslocamento = monstro.get("speed")
                if deslocamento:
                    for i in deslocamento:
                        dis = ''
                        if isinstance(deslocamento[i], int):
                            dis = deslocamento[i]
                        else:
                            dis = deslocamento[i].get("number")
                        
                        if dis:
                            dis = dis/5
                            
                            des = get_or_create(i, "deslocamentos", "deslocamento")
                            
                            conn.execute(
                                insert(metadata.tables["deslocamento_monstro"]).values({"deslocamento_id": des, "monstro_id": monstro_id, "distancia": dis})
                            )
                
                alinhamento = monstro.get("alignment")
                if alinhamento:
                    if isinstance(alinhamento, str):
                        alinhamento = bring_alignment(alinhamento)
                        if alinhamento:
                            ali = get_or_create(alinhamento, "alinhamentos", "alinhamento")
                            conn.execute(
                                insert(metadata.tables["alinhamento_monstro"]).values({"alinhamento_id": ali, "monstro_id": monstro_id})
                            )
                    else:
                        for i in alinhamento:
                            if isinstance(i, dict):
                                aux = i.get("alignment")
                                if not aux:
                                    continue
                                ali = bring_alignment(aux)
                            else:
                                ali = bring_alignment(i)
                            
                            if ali:
                                ali = get_or_create(ali, "alinhamentos", "alinhamento")
                                conn.execute(
                                    insert(metadata.tables["alinhamento_monstro"]).values({"alinhamento_id": ali, "monstro_id": monstro_id})
                                )
                
                pericias = monstro.get("skill")
                if pericias:
                    for i in pericias:
                        peri = get_or_create(i, "pericias", "pericia")
                        conn.execute(
                            insert(metadata.tables["pericia_monstro"]).values({"pericia_id": peri, "monstro_id": monstro_id})
                        )
                
                resistencias = monstro.get("resist")
                if resistencias:
                    for i in resistencias:
                        if isinstance(i, str):
                            dano = get_or_create(i, "danos", "dano")
                            conn.execute(
                                insert(metadata.tables["resistencia_monstro"]).values({"dano_id": dano, "monstro_id": monstro_id})
                            )
                        elif i.get("resist"):
                            for j in i["resist"]:
                                if isinstance(j, str):
                                    dano = get_or_create(j, "danos", "dano")
                                    conn.execute(
                                        insert(metadata.tables["resistencia_monstro"]).values({"dano_id": dano, "monstro_id": monstro_id})
                                    )
                                elif j.get("resist"):
                                    for k in j["resist"]:
                                        dano = get_or_create(k, "danos", "dano")
                                        conn.execute(
                                            insert(metadata.tables["resistencia_monstro"]).values({"dano_id": dano, "monstro_id": monstro_id})
                                        )
                
                vulnerabilidades = monstro.get("vulnerable")
                if vulnerabilidades:
                    for i in vulnerabilidades:
                        if isinstance(i, str):
                            dano = get_or_create(i, "danos", "dano")
                            conn.execute(
                                insert(metadata.tables["vulnerabilidade_monstro"]).values({"dano_id": dano, "monstro_id": monstro_id})
                            )
                        else:
                            for j in i["vulnerable"]:
                                dano = get_or_create(j, "danos", "dano")
                                conn.execute(
                                    insert(metadata.tables["vulnerabilidade_monstro"]).values({"dano_id": dano, "monstro_id": monstro_id})
                                )

                imunidades_dano = monstro.get("immune")
                if imunidades_dano:
                    for i in imunidades_dano:
                        if isinstance(i, str):
                            dano = get_or_create(i, "danos", "dano")
                            conn.execute(
                                insert(metadata.tables["imunidade_dano_monstro"]).values({"dano_id": dano, "monstro_id": monstro_id})
                            )
                        else:
                            aux = i.get("immune")
                            if aux:
                                for j in aux:
                                    dano = get_or_create(j, "danos", "dano")
                                    conn.execute(
                                        insert(metadata.tables["imunidade_dano_monstro"]).values({"dano_id": dano, "monstro_id": monstro_id})
                                    )

                imunidades_condicao = monstro.get("conditionImmune")
                if imunidades_condicao:
                    for i in imunidades_condicao:
                        if isinstance(i, str):
                            condicao = get_or_create(i, "condicoes", "condicao")
                            conn.execute(
                                insert(metadata.tables["imunidade_condicao_monstro"]).values({"condicao_id": condicao, "monstro_id": monstro_id})
                            )
                        else:
                            imuni = i.get("immune")
                            if not imuni:
                                imuni = i.get("conditionImmune")
                            for j in imuni:
                                condicao = get_or_create(j, "condicoes", "condicao")
                                conn.execute(
                                    insert(metadata.tables["imunidade_condicao_monstro"]).values({"condicao_id": condicao, "monstro_id": monstro_id})
                                )
                
                idiomas = monstro.get("languages")
                if idiomas:
                    for i in idiomas:
                        if i.count(" ") == 0:
                            idi = get_or_create(i, "idiomas", "idioma")
                            conn.execute(
                                insert(metadata.tables["idioma_monstro"]).values({"idioma_id": idi, "monstro_id": monstro_id})
                            )
                
                sentidos = monstro.get("senses")
                if sentidos:
                    for i in sentidos:
                        lista = i.split()
                        if len(lista) <= 3:
                            sen = get_or_create(lista[0], "sentidos", "sentido")
                            conn.execute(
                                insert(metadata.tables["sentido_monstro"]).values({"sentido_id": sen, "monstro_id": monstro_id, "distancia": int(re.sub(r'\D', '', lista[1]) )/5})
                            )

                habitats = monstro.get("environment")
                if habitats:
                    for i in habitats:
                        lista = i.split()
                        hab = get_or_create(lista[0], "habitats", "habitat")
                        conn.execute(
                            insert(metadata.tables["habitat_monstro"]).values({"habitat_id": hab, "monstro_id": monstro_id})
                        )

                if not tamanhos:
                    tamanhos = monstro.get("size")
                if tamanhos:
                    for i in tamanhos:
                        tam = get_or_create(i, "tamanhos", "tamanho")
                        conn.execute(
                            insert(metadata.tables["tamanho_monstro"]).values({"tamanho_id": tam, "monstro_id": monstro_id})
                        )

                conn.commit()
                conn.close()
            print("OK 2")
        print("OK 1")