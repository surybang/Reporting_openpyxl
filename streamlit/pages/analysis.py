import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from utils.data_loader import load_data


st.title("📊 Analyse des données clients")

df = load_data()

st.subheader("Répartition des types de clients")
st.bar_chart(df["type_client"].value_counts())

st.subheader("Adhésions dans le temps")
df["year"] = df["date_adhesion"].dt.year
adhesions_par_an = df.groupby("year").size()
st.line_chart(adhesions_par_an)

st.subheader("Matrice de transition des scores")
transition = pd.crosstab(df["score_prev"], df["score"])
fig, ax = plt.subplots()
sns.heatmap(transition, annot=True, fmt="d", cmap="Blues", ax=ax)
st.pyplot(fig)

st.subheader("Taux de DRC complété par type de client")
drc_rate = df.groupby("type_client")["drc_complet"].mean()
st.bar_chart(drc_rate)
