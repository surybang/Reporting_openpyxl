import streamlit as st

from utils.data_loader import load_data


st.title("🔎 Exploration interactive")

df = load_data()

type_sel = st.multiselect("Filtrer par type de client", df["type_client"].unique())
score_sel = st.multiselect("Filtrer par score", df["score"].unique())

df_filtred = df.copy()
if type_sel:
    df_filtred = df_filtred[df_filtred["type_client"].isin(type_sel)]
if score_sel:
    df_filtred = df_filtred[df_filtred["score"].isin(score_sel)]

st.dataframe(df_filtred)
