from common import init_page, load_clean_data, sidebar_filters, section_card
import plotly.express as px
import streamlit as st

init_page()

df = load_clean_data()
filtered = sidebar_filters(df)

section_card("Executive Overview", "High-level commercial KPIs for sales, profit, orders, discounts, and regional performance.")

total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()
total_orders = filtered["order_id"].nunique()
avg_discount = filtered["discount"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Avg Discount", f"{avg_discount:.1%}")

daily_sales = (
    filtered.groupby("order_date")["sales"]
    .sum()
    .reset_index()
    .sort_values("order_date")
)

fig = px.line(
    daily_sales,
    x="order_date",
    y="sales",
    title="Daily Sales Trend",
)
st.plotly_chart(fig, use_container_width=True)

region_summary = (
    filtered.groupby("region")
    .agg(
        Sales=("sales", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique"),
        Avg_Discount=("discount", "mean"),
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
)

st.markdown("### Regional Performance")
st.dataframe(region_summary, use_container_width=True)
