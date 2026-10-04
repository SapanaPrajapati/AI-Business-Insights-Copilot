import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# Find .env in the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


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
