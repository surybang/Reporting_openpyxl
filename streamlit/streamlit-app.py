import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load data
@st.cache_data
def load_data():
    return pd.read_parquet("data/data.parquet")


df = load_data()
df["date_adhesion"] = pd.to_datetime(df["date_adhesion"])

# ----------- SIDEBAR -----------
st.sidebar.title("📁 Reporting")
minio_url = "https://minio.lab.sspcloud.fr/fabienhos/Tuto_reporting/reporting.xlsx"
st.sidebar.markdown(f"[📥 Télécharger le reporting]({minio_url})")

# ----------- MAIN APP -----------
st.title("📊 Analyse des données clients")

st.subheader("1. Répartition des types de clients")
st.bar_chart(df["type_client"].value_counts())

st.subheader("2. Adhésions dans le temps")
df["year"] = df["date_adhesion"].dt.year
adhesions_par_an = df.groupby("year").size()
st.line_chart(adhesions_par_an)

st.subheader("3. Matrice de transition des scores")
transition = pd.crosstab(df["score_prev"], df["score"])

fig, ax = plt.subplots()
sns.heatmap(transition, annot=True, fmt="d", cmap="Blues", ax=ax)
st.pyplot(fig)

st.subheader("4. Taux de DRC complété par type de client")
drc_rate = df.groupby("type_client")["drc_complet"].mean()
st.bar_chart(drc_rate)

# ----------- FILTRAGE INTERACTIF -----------
st.subheader("5. Exploration personnalisée")

type_sel = st.multiselect("Filtrer par type de client", df["type_client"].unique())
score_sel = st.multiselect("Filtrer par score", df["score"].unique())

df_filtred = df.copy()
if type_sel:
    df_filtred = df_filtred[df_filtred["type_client"].isin(type_sel)]
if score_sel:
    df_filtred = df_filtred[df_filtred["score"].isin(score_sel)]

st.dataframe(df_filtred)

# Optionnel : téléchargement CSV
st.download_button(
    "📤 Télécharger les données filtrées",
    df_filtred.to_csv(index=False),
    file_name="data_filtred.csv",
)
