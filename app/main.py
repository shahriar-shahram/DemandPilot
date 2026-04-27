import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR / "src"))

from config import CLEAN_DATA_PATH, MODEL_METRICS_PATH, PREDICTIONS_PATH
from inference import predict_from_uploaded_csv


st.set_page_config(
    page_title="DemandPilot | Retail Demand Intelligence",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def load_clean_data():
    df = pd.read_csv(CLEAN_DATA_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


@st.cache_data
def load_metrics():
    return pd.read_csv(MODEL_METRICS_PATH)


@st.cache_data
def load_predictions():
    df = pd.read_csv(PREDICTIONS_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_clean_data()
metrics = load_metrics()
preds = load_predictions()

st.title("DemandPilot")
st.subheader("Retail Demand Forecasting and Business Intelligence Dashboard")

st.markdown(
    """
    DemandPilot is a client-ready retail analytics and forecasting system.
    It helps business users monitor sales performance, compare forecasting models,
    upload retail transaction data, and generate demand forecasts using a persisted
    machine-learning model.
    """
)

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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Executive Overview",
        "Demand Explorer",
        "Forecasting Lab",
        "Client Upload Forecast",
        "Profit & Discount",
        "Methodology",
    ]
)

with tab1:
    st.markdown("### Executive Summary")

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

with tab2:
    st.markdown("### Demand Explorer")

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

with tab3:
    st.markdown("### Forecasting Lab")

    st.markdown(
        """
        This section compares forecasting models using time-aware evaluation.
        Lower MAE, RMSE, SMAPE, and WAPE indicate better performance.
        Bias close to zero means the model has less systematic over- or under-forecasting.
        """
    )

    st.dataframe(metrics, use_container_width=True)

    best_model = metrics.sort_values("SMAPE").iloc[0]["model"]
    st.success(f"Best model by SMAPE: {best_model}")

    pred_models = sorted(preds["model"].unique())
    selected_model = st.selectbox(
        "Model",
        pred_models,
        index=pred_models.index(best_model) if best_model in pred_models else 0,
    )

    pred_regions = sorted(preds["Region"].dropna().unique())
    pred_categories = sorted(preds["Category"].dropna().unique())

    selected_pred_region = st.selectbox("Forecast Region", pred_regions)
    selected_pred_category = st.selectbox("Forecast Category", pred_categories)

    segment_preds = preds[
        (preds["model"] == selected_model)
        & (preds["Region"] == selected_pred_region)
        & (preds["Category"] == selected_pred_category)
    ].copy()

    segment_preds = segment_preds.sort_values("date")

    if segment_preds.empty:
        st.warning("No forecast records found for this segment.")
    else:
        fig = px.line(
            segment_preds,
            x="date",
            y=["total_sales", "prediction"],
            title=f"Actual vs Forecast: {selected_pred_region} / {selected_pred_category}",
        )
        st.plotly_chart(fig, use_container_width=True)

        segment_preds["absolute_error"] = (
            segment_preds["total_sales"] - segment_preds["prediction"]
        ).abs()

        fig = px.line(
            segment_preds,
            x="date",
            y="absolute_error",
            title="Forecast Error Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### Client Upload Forecast")

    st.markdown(
        """
        Upload a retail transaction CSV using the same schema as the training data.
        DemandPilot will validate the file, build forecasting features, load the saved
        production model, and generate demand forecasts at the region-category level.
        """
    )

    with st.expander("Required CSV columns"):
        st.code(
            """
order_date
region
product_category
sales
profit
discount
order_id
order_quantity
product_name
shipping_cost
unit_price
product_base_margin
            """.strip()
        )

    uploaded_file = st.file_uploader(
        "Upload client retail CSV",
        type=["csv"],
        help="Upload a CSV file with historical retail transactions.",
    )

    if uploaded_file is not None:
        try:
            forecast_output = predict_from_uploaded_csv(uploaded_file)

            st.success("Forecast generated successfully.")

            total_actual = forecast_output["total_sales"].sum()
            total_forecast = forecast_output["forecast_sales"].sum()
            mean_forecast = forecast_output["forecast_sales"].mean()
            num_segments = forecast_output[["Region", "Category"]].drop_duplicates().shape[0]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Historical Sales in Upload", f"${total_actual:,.0f}")
            col2.metric("Forecasted Sales", f"${total_forecast:,.0f}")
            col3.metric("Avg Forecast / Row", f"${mean_forecast:,.0f}")
            col4.metric("Forecast Segments", f"{num_segments:,}")

            st.markdown("### Forecast Preview")
            preview_cols = [
                "date",
                "Region",
                "Category",
                "total_sales",
                "forecast_sales",
            ]
            st.dataframe(forecast_output[preview_cols].head(100), use_container_width=True)

            daily_forecast = (
                forecast_output.groupby("date")
                .agg(
                    actual_sales=("total_sales", "sum"),
                    forecast_sales=("forecast_sales", "sum"),
                )
                .reset_index()
                .sort_values("date")
            )

            fig = px.line(
                daily_forecast,
                x="date",
                y=["actual_sales", "forecast_sales"],
                title="Uploaded Data: Actual vs Forecasted Sales",
            )
            st.plotly_chart(fig, use_container_width=True)

            segment_summary = (
                forecast_output.groupby(["Region", "Category"])
                .agg(
                    Actual_Sales=("total_sales", "sum"),
                    Forecast_Sales=("forecast_sales", "sum"),
                    Avg_Forecast=("forecast_sales", "mean"),
                )
                .reset_index()
                .sort_values("Forecast_Sales", ascending=False)
            )

            st.markdown("### Segment Forecast Summary")
            st.dataframe(segment_summary, use_container_width=True)

            csv = forecast_output.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Forecast CSV",
                data=csv,
                file_name="demandpilot_forecast_output.csv",
                mime="text/csv",
            )

        except Exception as exc:
            st.error("Forecast generation failed.")
            st.exception(exc)

with tab5:
    st.markdown("### Profit and Discount Analysis")

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

with tab6:
    st.markdown("### Methodology")

    st.markdown(
        """
        **Pipeline**

        1. Clean raw retail transaction data.
        2. Aggregate transactions into daily region-category demand.
        3. Build time-series features using calendar variables, lagged sales,
           rolling demand statistics, discount, profit, margin, shipping cost,
           and order-volume signals.
        4. Compare simple forecasting baselines against machine-learning models.
        5. Save the best model as a backend inference artifact.
        6. Support client CSV upload for forecast generation.
        7. Visualize demand, profit, forecast error, and model comparison in an
           interactive dashboard.

        **Models**

        - Naive lag-1 baseline
        - Seasonal naive lag-7 baseline
        - Rolling mean baseline
        - Linear Regression
        - Ridge Regression
        - Random Forest
        - Histogram-based Gradient Boosting

        **Metrics**

        - MAE: average absolute error
        - RMSE: root mean squared error
        - SMAPE: symmetric mean absolute percentage error
        - WAPE: total absolute error relative to total demand
        - Bias: systematic over- or under-forecasting

        **Cloud Readiness**

        - Dockerfile included for containerized deployment.
        - AWS deployment plan included for App Runner, ECS/Fargate, or Elastic Beanstalk.
        - Future production version can move uploaded files and model artifacts to S3.
        """
    )
