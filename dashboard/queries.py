import pandas as pd
from db import engine

def read(q):
    return pd.read_sql(q, engine)


# 1 habitat
def monstros_por_habitat():
    return read("""
        SELECT h.habitat, COUNT(*) AS total
        FROM monstros m
        JOIN habitat_monstro hm ON m.id = hm.monstro_id
        JOIN habitats h ON hm.habitat_id = h.id
        GROUP BY h.habitat
    """)

# 2 tipo
def monstros_por_tipo():
    return read("""
        SELECT t.tipo, COUNT(*) AS total
        FROM monstros m
        JOIN tipos t ON m.tipo_id = t.id
        GROUP BY t.tipo
    """)

# 3 alinhamento
def monstros_por_alinhamento():
    return read("""
        SELECT a.alinhamento, COUNT(*) AS total
        FROM monstros m
        JOIN alinhamento_monstro am ON m.id = am.monstro_id
        JOIN alinhamentos a ON am.alinhamento_id = a.id
        GROUP BY a.alinhamento
    """)

# 4 tamanho
def monstros_por_tamanho():
    return read("""
        SELECT t.tamanho, COUNT(*) AS total
        FROM monstros m
        JOIN tamanho_monstro tm ON m.id = tm.monstro_id
        JOIN tamanhos t ON tm.tamanho_id = t.id
        GROUP BY t.tamanho
    """)

# 4 vulnerabilidade
def vulnerabilidade():
    return read("""
        SELECT d.dano, COUNT(DISTINCT vm.monstro_id) AS total
        FROM vulnerabilidade_monstro vm
        JOIN danos d ON vm.dano_id = d.id
        GROUP BY d.dano
        ORDER BY total DESC
        LIMIT 10
    """)

# 5 resistência
def resistencia():
    return read("""
        SELECT 
            d.dano,
            COUNT(DISTINCT CASE WHEN rm.nao_magico = FALSE THEN rm.monstro_id END) AS resistencia_normal,
            COUNT(DISTINCT CASE WHEN rm.nao_magico = TRUE THEN rm.monstro_id END) AS resistencia_nonmagica,
            COUNT(DISTINCT rm.monstro_id) AS total
        FROM resistencia_monstro rm
        JOIN danos d ON rm.dano_id = d.id
        GROUP BY d.dano
        ORDER BY total DESC
        LIMIT 10
    """)

# 6 imunidade
def imunidade():
    return read("""
        SELECT 
            d.dano,
            COUNT(DISTINCT CASE WHEN im.nao_magico = FALSE THEN im.monstro_id END) AS imunidade_normal,
            COUNT(DISTINCT CASE WHEN im.nao_magico = TRUE THEN im.monstro_id END) AS imunidade_nonmagica,
            COUNT(DISTINCT im.monstro_id) AS total
        FROM imunidade_dano_monstro im
        JOIN danos d ON im.dano_id = d.id
        GROUP BY d.dano
        ORDER BY total DESC
        LIMIT 10
    """)

# base para ranking completo
def tabela_danos():
    return read("""
        SELECT 
            d.dano,

            COALESCE(v.qtd_vulnerabilidade, 0) AS qtd_vulnerabilidade,

            COALESCE(r.magica, 0) AS qtd_resistencia_magica,
            COALESCE(r.nao_magica, 0) AS qtd_resistencia_nao_magica,

            COALESCE(i.magica, 0) AS qtd_imunidade_magica,
            COALESCE(i.nao_magica, 0) AS qtd_imunidade_nao_magica

        FROM danos d

        LEFT JOIN (
            SELECT dano_id, COUNT(*) AS qtd_vulnerabilidade
            FROM vulnerabilidade_monstro
            GROUP BY dano_id
        ) v ON v.dano_id = d.id

        LEFT JOIN (
            SELECT 
                dano_id,
                SUM(CASE WHEN nao_magico = FALSE THEN 1 ELSE 0 END) AS magica,
                SUM(CASE WHEN nao_magico = TRUE THEN 1 ELSE 0 END) AS nao_magica
            FROM resistencia_monstro
            GROUP BY dano_id
        ) r ON r.dano_id = d.id

        LEFT JOIN (
            SELECT 
                dano_id,
                SUM(CASE WHEN nao_magico = FALSE THEN 1 ELSE 0 END) AS magica,
                SUM(CASE WHEN nao_magico = TRUE THEN 1 ELSE 0 END) AS nao_magica
            FROM imunidade_dano_monstro
            GROUP BY dano_id
        ) i ON i.dano_id = d.id;
    """)

# magias
def magias_escola():
    return read("""
        SELECT e.escola, COUNT(*) total
        FROM magias m
        JOIN escolas e ON m.escola_id = e.id
        GROUP BY e.escola
    """)

def magias_nivel():
    return read("""
        SELECT nivel, COUNT(*) total
        FROM magias
        GROUP BY nivel
    """)

def dano_magia():
    return read("""
        SELECT m.nome, d.dano, dm.media
        FROM dano_magia dm
        JOIN magias m ON dm.magia_id = m.id
        JOIN danos d ON dm.dano_id = d.id
    """)