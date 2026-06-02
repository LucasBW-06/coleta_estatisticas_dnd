import streamlit as st
import altair as alt
import pandas as pd

import queries as q

st.set_page_config(page_title="Dashboard D&D", layout="wide")

st.title("📊 Estatísticas D&D - Dashboard")

# =========================
# 1 HABITATS
# =========================
st.header("1) Monstros por Habitat")

df = q.monstros_por_habitat()

df["percentual"] = df["total"] / df["total"].sum() * 100

chart = alt.Chart(df).mark_arc().encode(
    theta="total",
    color=alt.Color("habitat", title="Habitat"),
    tooltip=[  
    alt.Tooltip("habitat", title="Habitat"),
    alt.Tooltip("total", title="Nº de Monstros"),
    alt.Tooltip("percentual", title="% do Total", format=".2f")]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 2 TIPOS
# =========================
st.header("2) Monstros por Tipo")

df = q.monstros_por_tipo()

df["percentual"] = df["total"] / df["total"].sum() * 100

chart = alt.Chart(df).mark_arc().encode(
    theta="total",
    color=alt.Color("tipo", title="Tipo"),
    tooltip=[  
    alt.Tooltip("tipo", title="Tipo"),
    alt.Tooltip("total", title="Nº de Monstros"),
    alt.Tooltip("percentual", title="% do Total", format=".2f")]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 3 ALINHAMENTO
# =========================
st.header("3) Monstros por Alinhamento")

df = q.monstros_por_alinhamento()

df["percentual"] = df["total"] / df["total"].sum() * 100

chart = alt.Chart(df).mark_arc().encode(
    theta="total",
    color=alt.Color("alinhamento", title="Alinhamento"),
    tooltip=[  
    alt.Tooltip("alinhamento", title="Alinhamento"),
    alt.Tooltip("total", title="Nº de Monstros"),
    alt.Tooltip("percentual", title="% do Total", format=".2f")]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 4 TAMANHO
# =========================
st.header("4) Monstros por Tamanho")

df = q.monstros_por_tamanho()

df["percentual"] = df["total"] / df["total"].sum() * 100

chart = alt.Chart(df).mark_arc().encode(
    theta="total",
    color=alt.Color("tamanho", title="Tamanho"),
    tooltip=[  
    alt.Tooltip("tamanho", title="Tamanho"),
    alt.Tooltip("total", title="Nº de Monstros"),
    alt.Tooltip("percentual", title="% do Total", format=".2f")]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 4 VULNERABILIDADE
# =========================
st.header("4) Top 10 Vulnerabilidades")

df = q.vulnerabilidade()

chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("total:Q", title="Nº de Monstros"),
    y=alt.Y("dano:N", sort="-x", title="Dano"),
    tooltip=[
    alt.Tooltip("dano", title="Dano"),
    alt.Tooltip("total", title="Nº de Monstros")]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 5 RESISTÊNCIA
# =========================
st.header("5) Top 10 Resistências")

df = q.resistencia()

df_long = df.melt(
    id_vars=["dano"],
    value_vars=["resistencia_normal", "resistencia_nonmagica"],
    var_name="tipo",
    value_name="quantidade"
)

df_long = df_long[df_long["quantidade"] > 0]

# renomear para ficar bonito no gráfico
df_long["tipo"] = df_long["tipo"].replace({
    "resistencia_normal": "normal",
    "resistencia_nonmagica": "nonmagical"
})

df_long["dano_tipo"] = df_long.apply(
    lambda row: (
        row["dano"] + " (nonmagical)"
        if row["tipo"] == "nonmagical"
        else row["dano"]
    ),
    axis=1
)

chart = alt.Chart(df_long).mark_bar().encode(
    x=alt.X("quantidade:Q", title="Nº de Monstros"),
    y=alt.Y("dano_tipo:N", sort="-x", title="Dano"),
    tooltip=[
        alt.Tooltip("dano", title="Dano"),
        alt.Tooltip("tipo", title="Tipo"),
        alt.Tooltip("quantidade", title="Nº de Monstros")
    ]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 6 IMUNIDADE
# =========================
st.header("6) Top 10 Imunidades")

df = q.imunidade()

df_long = df.melt(
    id_vars=["dano"],
    value_vars=["imunidade_normal", "imunidade_nonmagica"],
    var_name="tipo",
    value_name="quantidade"
)

df_long = df_long[df_long["quantidade"] > 0]

# renomear para ficar bonito no gráfico
df_long["tipo"] = df_long["tipo"].replace({
    "imunidade_normal": "normal",
    "imunidade_nonmagica": "nonmagical"
})

df_long["dano_tipo"] = df_long.apply(
    lambda row: (
        row["dano"] + " (nonmagical)"
        if row["tipo"] == "nonmagical"
        else row["dano"]
    ),
    axis=1
)

chart = alt.Chart(df_long).mark_bar().encode(
    x=alt.X("quantidade:Q", title="Nº de Monstros"),
    y=alt.Y("dano_tipo:N", sort="-x", title="Dano"),
    tooltip=[
        alt.Tooltip("dano", title="Dano"),
        alt.Tooltip("tipo", title="Tipo"),
        alt.Tooltip("quantidade", title="Nº de Monstros")
    ]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 7 TABELA RANKING
# =========================
st.header("7) Ranking de Tipos de Dano")

df_rank = q.tabela_danos()

df_nm = df_rank[
    (df_rank["qtd_resistencia_nao_magica"] > 0) |
    (df_rank["qtd_imunidade_nao_magica"] > 0)
].copy()

df_nm["dano"] = df_nm["dano"] + " (nonmagical)"

df_nm["resistencia"] = df_nm["qtd_resistencia_nao_magica"]
df_nm["imunidade"] = df_nm["qtd_imunidade_nao_magica"]

df_nm["vulnerabilidade"] = df_nm["qtd_vulnerabilidade"]

df_nm = df_nm[["dano", "vulnerabilidade", "resistencia", "imunidade"]]

df_mag = df_rank.copy()

df_mag = df_mag.rename(columns={
    "qtd_vulnerabilidade": "vulnerabilidade",
    "qtd_resistencia_magica": "resistencia",
    "qtd_imunidade_magica": "imunidade"
})

df_mag = df_mag[["dano", "vulnerabilidade", "resistencia", "imunidade"]]

df_rank = pd.concat([df_mag, df_nm], ignore_index=True)

st.subheader("Pesos do ranking")

w_v = st.slider("Peso vulnerabilidade", -1.0, 5.0, 1.0, 0.5)
w_r = st.slider("Peso resistência", -1.0, 5.0, 1.0, 0.5)
w_i = st.slider("Peso imunidade", -1.0, 5.0, 1.0, 0.5)

df_rank["score"] = (
    df_rank["vulnerabilidade"].rank(ascending=False) * w_v -
    df_rank["resistencia"].rank(ascending=False) * w_r -
    df_rank["imunidade"].rank(ascending=False) * w_i
)

df_rank = df_rank.sort_values("score")

st.dataframe(df_rank)

# =========================
# 8 MAGIAS POR ESCOLA
# =========================
st.header("8) Magias por Escola")

df = q.magias_escola()

df["percentual"] = df["total"] / df["total"].sum() * 100

chart = alt.Chart(df).mark_arc().encode(
    theta="total",
    color=alt.Color("escola", title="Escola"),
    tooltip=[  
    alt.Tooltip("escola", title="Escola"),
    alt.Tooltip("total", title="Nº de Magias"),
    alt.Tooltip("percentual", title="% do Total", format=".2f")]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 9 MAGIAS POR NÍVEL
# =========================
st.header("9) Magias por Nível")

df = q.magias_nivel()

df["percentual"] = df["total"] / df["total"].sum() * 100

chart = alt.Chart(df).mark_arc().encode(
    theta="total",
    color=alt.Color("nivel", title="Nível"),
    tooltip=[  
    alt.Tooltip("nivel", title="Nível"),
    alt.Tooltip("total", title="Nº de Magias"),
    alt.Tooltip("percentual", title="% do Total", format=".2f")]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 10 MELHORES MAGIAS DO TOP DANO
# =========================
st.header("10) Magias mais fortes (ajustado por tipo de dano)")

df_magia = q.dano_magia()

# remove nonmagical do ranking
df_rank_clean = df_rank[~df_rank["dano"].str.contains(r"\(nonmagical\)", na=False)].copy()

# TOP DANO (somente magical)
top_dano = df_rank_clean.iloc[0]["dano"]

# lista de danos (limpa)
todos_danos = sorted(df_rank_clean["dano"].unique())

# opções do seletor
options = ["all"] + [
    f"{dano} (top)" if dano == top_dano else dano
    for dano in todos_danos
]

# seletor
selected = st.selectbox("Escolha o tipo de dano", options)

# lógica de filtro
if selected == "all":
    df = df_magia.copy()

elif "(top)" in selected:
    dano_escolhido = selected.replace(" (top)", "")
    df = df_magia[df_magia["dano"] == dano_escolhido]

else:
    df = df_magia[df_magia["dano"] == selected]

# ordena e pega top 10
df = df.sort_values("media", ascending=False).head(10)

# gráfico
chart = alt.Chart(df).mark_bar().encode(
    x="media:Q",
    y=alt.Y("nome:N", sort="-x"),
    tooltip=["nome", "dano", "media"]
)

st.altair_chart(chart, use_container_width=True)

# =========================
# 11 MELHORES MAGIAS GLOBAL
# =========================
st.header("11) Top 10 Magias (score global ajustado)")

df = df_magia.copy()

df["score_dano"] = df["dano"].map(
    df_rank.set_index("dano")["score"]
)

df["valor"] = df["media"] - df["score_dano"]

df = df.sort_values("valor", ascending=False).head(10)

chart = alt.Chart(df).mark_bar().encode(
    x="valor:Q",
    y=alt.Y("nome:N", sort="-x"),
    color="dano",
    tooltip=["nome", "dano", "media", "valor"]
)

st.altair_chart(chart, use_container_width=True)