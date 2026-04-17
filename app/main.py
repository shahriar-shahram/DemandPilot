import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DemandPilot Dashboard", layout="wide")

st.title("DemandPilot Dashboard")
st.write("Retail sales analytics and demand signal exploration")

# =========================
# Load data
# =========================
df = pd.read_csv("data/processed/clean_data.csv")
daily_sales = pd.read_csv("data/processed/daily_sales.csv")

df["order_date"] = pd.to_datetime(df["order_date"])
daily_sales["order_date"] = pd.to_datetime(daily_sales["order_date"])

# =========================
# Sidebar filters
# =========================
st.sidebar.header("Filters")

regions = sorted(df["region"].dropna().unique().tolist()) if "region" in df.columns else []
categories = sorted(df["product_category"].dropna().unique().tolist()) if "product_category" in df.columns else []

selected_regions = st.sidebar.multiselect("Select Region(s)", regions, default=regions)
selected_categories = st.sidebar.multiselect("Select Category(s)", categories, default=categories)

filtered_df = df.copy()

if "region" in filtered_df.columns and selected_regions:
    filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

if "product_category" in filtered_df.columns and selected_categories:
    filtered_df = filtered_df[filtered_df["product_category"].isin(selected_categories)]

# Recompute filtered daily sales
filtered_daily_sales = (
    filtered_df.groupby("order_date")["sales"]
    .sum()
    .reset_index()
    .sort_values("order_date")
)

# Monthly sales
monthly_sales = (
    filtered_df.set_index("order_date")
    .resample("M")["sales"]
    .sum()
    .reset_index()
)

# =========================
# KPI Section
# =========================
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum() if "profit" in filtered_df.columns else 0
total_orders = filtered_df["order_id"].nunique() if "order_id" in filtered_df.columns else len(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")

st.divider()

# =========================
# Daily Sales Trend
# =========================
st.subheader("Daily Sales Trend")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(filtered_daily_sales["order_date"], filtered_daily_sales["sales"])
ax.set_xlabel("Order Date")
ax.set_ylabel("Sales")
ax.set_title("Filtered Daily Sales Over Time")
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()

# =========================
# Monthly Sales Trend
# =========================
st.subheader("Monthly Sales Trend")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(monthly_sales["order_date"], monthly_sales["sales"])
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.set_title("Monthly Sales")
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()

# =========================
# Profit by Region
# =========================
if "region" in filtered_df.columns and "profit" in filtered_df.columns:
    st.subheader("Profit by Region")
    region_profit = filtered_df.groupby("region")["profit"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 4))
    region_profit.plot(kind="bar", ax=ax)
    ax.set_ylabel("Profit")
    ax.set_title("Total Profit by Region")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()

# =========================
# Discount vs Profit
# =========================
if "discount" in filtered_df.columns and "profit" in filtered_df.columns:
    st.subheader("Discount vs Profit")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(filtered_df["discount"], filtered_df["profit"], alpha=0.5)
    ax.set_xlabel("Discount")
    ax.set_ylabel("Profit")
    ax.set_title("Discount vs Profit")
    st.pyplot(fig)

st.divider()

# =========================
# Top Products Table
# =========================
if "product_name" in filtered_df.columns:
    st.subheader("Top 10 Products by Sales")
    top_products = (
        filtered_df.groupby("product_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    st.dataframe(top_products, use_container_width=True)

st.divider()

# =========================
# Regional Forecasting
# =========================
st.subheader("Regional Forecasting")

forecast_region_df = pd.read_csv("data/processed/forecast_results_by_region.csv")
forecast_region_df["order_date"] = pd.to_datetime(forecast_region_df["order_date"])

metrics_region_df = pd.read_csv("data/processed/forecast_metrics_by_region.csv")

region_options = forecast_region_df["region"].unique()
selected_region = st.selectbox("Select Region", region_options)

region_data = forecast_region_df[forecast_region_df["region"] == selected_region]
region_metrics = metrics_region_df[metrics_region_df["region"] == selected_region]

col1, col2, col3 = st.columns(3)
col1.metric("MAE", f"{region_metrics['MAE'].values[0]:.2f}")
col2.metric("RMSE", f"{region_metrics['RMSE'].values[0]:.2f}")
col3.metric("SMAPE", f"{region_metrics['SMAPE'].values[0]:.2f}%")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(region_data["order_date"], region_data["total_sales"], label="Actual")
ax.plot(region_data["order_date"], region_data["prediction"], label="Forecast")
ax.set_title(f"{selected_region} Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()

# =========================
# Category Forecasting
# =========================
st.subheader("Category Forecasting")

forecast_category_df = pd.read_csv("data/processed/forecast_results_by_category.csv")
forecast_category_df["order_date"] = pd.to_datetime(forecast_category_df["order_date"])

metrics_category_df = pd.read_csv("data/processed/forecast_metrics_by_category.csv")

category_options = forecast_category_df["product_category"].unique()
selected_category = st.selectbox("Select Category", category_options)

category_data = forecast_category_df[forecast_category_df["product_category"] == selected_category]
category_metrics = metrics_category_df[metrics_category_df["product_category"] == selected_category]

col1, col2, col3 = st.columns(3)
col1.metric("MAE", f"{category_metrics['MAE'].values[0]:.2f}")
col2.metric("RMSE", f"{category_metrics['RMSE'].values[0]:.2f}")
col3.metric("SMAPE", f"{category_metrics['SMAPE'].values[0]:.2f}%")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(category_data["order_date"], category_data["total_sales"], label="Actual")
ax.plot(category_data["order_date"], category_data["prediction"], label="Forecast")
ax.set_title(f"{selected_category} Forecast")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)