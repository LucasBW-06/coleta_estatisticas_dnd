from sqlalchemy import create_engine

username = "root"
password = "admin"
host = "localhost"
port = 3306
database = "estatisticas_dnd"

connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string, echo=False)