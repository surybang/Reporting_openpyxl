import streamlit as st

st.title("🏠 Tableau de bord - Accueil")

st.markdown("""
Bienvenue sur l'application de reporting.  
Utilisez le menu de gauche pour naviguer entre les différentes analyses :
- Qualité des données
- Analyse des clients
- Exploration interactive
""")

st.title("📥 Téléchargement du reporting")

minio_url = "https://minio.lab.sspcloud.fr/fabienhos/Tuto_reporting/reporting.xlsx"

st.markdown("Vous pouvez télécharger le fichier de reporting ici :")
st.markdown(f"[📊 Télécharger le reporting Excel]({minio_url})", unsafe_allow_html=True)