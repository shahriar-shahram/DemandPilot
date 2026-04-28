from common import init_page, load_clean_data, sidebar_filters, section_card
import plotly.express as px
import streamlit as st

init_page()

df = load_clean_data()
filtered = sidebar_filters(df)

section_card("Profit & Discount Intelligence", "Analyze whether discounting, margin, and product category behavior support profitable demand generation.")

fig = px.scatter(
    filtered,
    x="discount",
    y="profit",
    color="product_category",
    size="sales",
    hover_data=["region", "product_name"],
    title="Discount vs Profit",
)
st.plotly_chart(fig, use_container_width=True)

profit_by_category = (
    filtered.groupby("product_category")
    .agg(
        Sales=("sales", "sum"),
        Profit=("profit", "sum"),
        Avg_Discount=("discount", "mean"),
        Avg_Margin=("product_base_margin", "mean"),
    )
    .reset_index()
)

fig = px.bar(
    profit_by_category,
    x="product_category",
    y="Profit",
    title="Profit by Product Category",
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(profit_by_category, use_container_width=True)
