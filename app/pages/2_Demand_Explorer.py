from common import init_page, load_clean_data, sidebar_filters, section_card
import plotly.express as px
import streamlit as st

init_page()

df = load_clean_data()
filtered = sidebar_filters(df)

section_card("Demand Explorer", "Explore monthly demand patterns, category mix, regional sales concentration, and top product performance.")

monthly = filtered.copy()
monthly["month"] = monthly["order_date"].dt.to_period("M").astype(str)

monthly_sales = (
    monthly.groupby(["month", "product_category"])["sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly_sales,
    x="month",
    y="sales",
    color="product_category",
    title="Monthly Sales by Product Category",
)
st.plotly_chart(fig, use_container_width=True)

category_region = (
    filtered.groupby(["region", "product_category"])["sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_region,
    x="region",
    y="sales",
    color="product_category",
    barmode="group",
    title="Sales by Region and Product Category",
)
st.plotly_chart(fig, use_container_width=True)

top_products = (
    filtered.groupby("product_name")
    .agg(
        Sales=("sales", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique"),
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(15)
)

st.markdown("### Top Products")
st.dataframe(top_products, use_container_width=True)
