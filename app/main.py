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

apply_brand_style()
render_brand_header()

section_card(
    "Retail forecasting, redesigned as a client product",
    "Monitor demand, compare forecasting models, upload client transaction data, and generate region-category forecasts through a persisted scikit-learn backend model."
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


with st.sidebar:
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio(
        "Choose a workspace",
        [
            "Home",
            "Executive Overview",
            "Demand Explorer",
            "Forecasting Lab",
            "Client Upload Forecast",
            "Profit & Discount",
            "Methodology",
        ],
        label_visibility="collapsed",
    )

if page == "Home":
    section_card(
        "What is DemandPilot?",
        "DemandPilot is a client-ready retail demand intelligence product. It turns historical transaction data into executive KPIs, demand forecasts, model evaluation reports, and upload-based forecasting workflows."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="dp-section-card">
              <div class="dp-section-title">Problem</div>
              <div class="dp-section-copy">
                Retail teams need to anticipate demand across regions and product categories,
                but transaction data is usually fragmented across sales, discounts, margins,
                shipping cost, and product behavior.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="dp-section-card">
              <div class="dp-section-title">Solution</div>
              <div class="dp-section-copy">
                DemandPilot builds a daily forecasting panel, engineers time-series and business
                features, compares baseline and ML models, and serves forecasts through a live dashboard.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="dp-section-card">
              <div class="dp-section-title">Impact</div>
              <div class="dp-section-copy">
                The product helps business users understand demand risk, compare forecasting models,
                and generate forecasts from client-uploaded retail transaction files.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Product Workflow")

    st.markdown(
        """
        <div class="dp-section-card">
          <div class="dp-section-title">From raw retail transactions to forecast-ready decisions</div>
          <div class="dp-section-copy">
            <b>1.</b> Clean and standardize historical retail data<br>
            <b>2.</b> Aggregate demand by date, region, and product category<br>
            <b>3.</b> Build lag, rolling, calendar, discount, profit, margin, and shipping features<br>
            <b>4.</b> Compare naive baselines, linear models, and nonlinear tree-based ML models<br>
            <b>5.</b> Persist the best model as a backend inference artifact<br>
            <b>6.</b> Let users upload client CSV files and download forecast outputs
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Best Model", "Random Forest")
    col2.metric("SMAPE", "17.1%")
    col3.metric("Forecast Level", "Region × Category")
    col4.metric("Deployment", "Live App")

    st.markdown("### Why this matters")

    st.markdown(
        """
        <div class="dp-section-card">
          <div class="dp-section-title">Business value</div>
          <div class="dp-section-copy">
            Demand forecasting is not only a modeling task. It affects inventory planning,
            promotion strategy, staffing, purchasing, and revenue risk. DemandPilot frames
            forecasting as a product workflow: users can inspect trends, compare models,
            upload data, and export forecast results.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Open the workspaces from the sidebar")

    st.markdown(
        """
        <div class="dp-pill-row">
            <div class="dp-pill"><strong>Executive Overview</strong> KPI monitoring</div>
            <div class="dp-pill"><strong>Demand Explorer</strong> trend discovery</div>
            <div class="dp-pill"><strong>Forecasting Lab</strong> model comparison</div>
            <div class="dp-pill"><strong>Client Upload</strong> model inference</div>
            <div class="dp-pill"><strong>Profit & Discount</strong> margin intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif page == "Executive Overview":
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

elif page == "Demand Explorer":
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

elif page == "Forecasting Lab":
    section_card("Forecasting Lab", "Compare model performance, inspect actual-vs-forecast behavior, and analyze forecast errors over time.")

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

    preds = load_predictions()
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

elif page == "Client Upload Forecast":
    section_card("Client Upload Forecast", "Upload a client retail CSV and generate forecasts using the saved backend model artifact.")

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

elif page == "Profit & Discount":
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

elif page == "Methodology":
    section_card("Methodology", "A productized ML workflow: data cleaning, feature engineering, model comparison, persisted inference, Docker, and AWS deployment planning.")

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
