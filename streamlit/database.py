import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


@st.cache_resource
def get_engine():

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return engine


@st.cache_data(ttl=600)
def load_data(query):

    engine = get_engine()

    return pd.read_sql(query, engine)