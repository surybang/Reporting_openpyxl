import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_parquet("data/data.parquet")
    df["date_adhesion"] = pd.to_datetime(df["date_adhesion"])
    return df
