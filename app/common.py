import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR / "src"))

from config import CLEAN_DATA_PATH, MODEL_METRICS_PATH, PREDICTIONS_PATH
from inference import predict_from_uploaded_csv
from styles import apply_brand_style, render_brand_header, section_card


st.set_page_config(
    page_title="DemandPilot | Retail Demand Intelligence",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def load_clean_data():
    usecols = [
        "order_date",
        "region",
        "product_category",
        "sales",
        "profit",
        "order_id",
        "discount",
        "product_name",
        "product_base_margin",
    ]
    df = pd.read_csv(CLEAN_DATA_PATH, usecols=usecols)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


@st.cache_data
def load_metrics():
    return pd.read_csv(MODEL_METRICS_PATH)


@st.cache_data
def load_predictions():
    usecols = ["date", "Region", "Category", "total_sales", "prediction", "model"]
    df = pd.read_csv(PREDICTIONS_PATH, usecols=usecols)
    df["date"] = pd.to_datetime(df["date"])
    return df


def init_page():
    apply_brand_style()
    render_brand_header()


def sidebar_filters(df):
    with st.sidebar:
        st.header("Business Filters")

        regions = sorted(df["region"].dropna().unique())
        categories = sorted(df["product_category"].dropna().unique())

        selected_regions = st.multiselect("Region", regions, default=regions)
        selected_categories = st.multiselect("Product Category", categories, default=categories)

        date_min = df["order_date"].min()
        date_max = df["order_date"].max()

        date_range = st.date_input(
            "Date Range",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max,
        )

    filtered = df[
        (df["region"].isin(selected_regions))
        & (df["product_category"].isin(selected_categories))
    ].copy()

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["order_date"] >= pd.to_datetime(start_date))
            & (filtered["order_date"] <= pd.to_datetime(end_date))
        ]

    return filtered
