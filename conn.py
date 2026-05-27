import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:Vehapraha%402010@localhost:3306/first_proj"
)
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        st.success("Database Connected Successfully!")
except Exception as e:
    st.error("Connection Failed");
st

