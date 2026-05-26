import requests

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

data = requests.get(
    "https://5e.tools/data/bestiary/bestiary-xmm.json"
).json()

print(data["monster"])