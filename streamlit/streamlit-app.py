import streamlit as st

pages = {
    "🏠 Accueil": [st.Page("pages/home.py", title="👨🏻‍💻 Informations")],

    "📊 Reporting": [
        st.Page("pages/quality.py", title="🧹 Qualité des données"),
        st.Page("pages/analysis.py", title="📊 Analyse des clients"),
        st.Page("pages/exploration.py", title="🔎 Exploration interactive"),
    ],
}

nav = st.navigation(pages)
nav.run()
