# import os
# import pandas as pd
# import streamlit as st
# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# from pathlib import Path

# # Find .env in the main project folder
# BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(BASE_DIR / ".env")

# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")


# @st.cache_resource
# def get_engine():

#     engine = create_engine(
#         f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
#         f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     )

#     return engine


# @st.cache_data(ttl=600)
# def load_data(query):

#     engine = get_engine()

#     return pd.read_sql(query, engine)


import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# Load the .env file from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_FILE)


def get_setting(name, default=None):
    """Read Streamlit Cloud Secrets first, then local environment variables."""
    try:
        value = st.secrets.get(name)
    except Exception:
        # Local environments may not have a Streamlit secrets file.
        value = None

    if value is not None and str(value).strip():
        return str(value).strip()

    value = os.getenv(name)

    if value is not None and value.strip():
        return value.strip()

    return default


@st.cache_resource
def get_engine():
    """Create and cache the MySQL database engine."""

    db_host = get_setting("DB_HOST")
    db_user = get_setting("DB_USER")
    db_password = get_setting("DB_PASSWORD")
    db_name = get_setting("DB_NAME")

    # Default to the standard MySQL port if it is missing or set to None.
    db_port_value = get_setting("DB_PORT", "3306")

    if db_port_value.lower() == "none":
        db_port_value = "3306"

    try:
        db_port = int(db_port_value)
        if not 1 <= db_port <= 65535:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError(
            "DB_PORT must be a valid port number, such as 3306."
        )

    missing = [
        name
        for name, value in {
            "DB_HOST": db_host,
            "DB_USER": db_user,
            "DB_PASSWORD": db_password,
            "DB_NAME": db_name,
        }.items()
        if not value
    ]

    if missing:
        raise ValueError(
            "Missing MySQL configuration: "
            + ", ".join(missing)
            + ". Configure these values in your local .env file "
            "or Streamlit Cloud Secrets."
        )

    # URL.create safely handles special characters in passwords.
    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name,
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True,
        pool_recycle=3600,
    )


@st.cache_data(ttl=600)
def load_data(query):
    """Run a SQL query and cache its results for 10 minutes."""
    engine = get_engine()
    return pd.read_sql(query, engine)

