import streamlit as st

from utils.data_loader import load_data


st.title("✅ Qualité de données")

df = load_data()

st.subheader("🔍 Taux de complétion des colonnes")
completion_rate = df.notnull().mean().sort_values()
st.bar_chart(completion_rate)

st.subheader("🧬 Lignes en double")
duplicated_count = df.duplicated().sum()
st.write(f"Nombre de lignes dupliquées : {duplicated_count}")
