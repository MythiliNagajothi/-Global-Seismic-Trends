import streamlit as st
import pandas as pd
from sqlalchemy import text
from conn import engine
from queries import queries

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Earthquake Dashboard",
    layout="wide"
)

st.title("🌍 Earthquake Analytics Dashboard")

# -----------------------------
# TEST CONNECTION
# -----------------------------
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        

except Exception as e:
    st.error("❌ Connection Failed")
    st.exception(e)

# -----------------------------
# SIDEBAR
# -----------------------------
query_name = st.sidebar.selectbox(
    "Select Analysis",
    list(queries.keys())
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

# -----------------------------
# FETCH DATA
# -----------------------------
df = load_data(queries[query_name])

# -----------------------------
# DISPLAY DATA
# -----------------------------
st.subheader(query_name)

st.dataframe(
    df,
    width='stretch'
)

# -----------------------------
# SHOW CHART
# -----------------------------
numeric_cols = df.select_dtypes(include='number').columns

if len(df.columns) >= 2 and len(numeric_cols) > 0:

    x_col = df.columns[1]
    y_col = numeric_cols[0]

    st.bar_chart(
        data=df,
        x=x_col,
        y=y_col
    )

# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "earthquake_data.csv",
    "text/csv"
)