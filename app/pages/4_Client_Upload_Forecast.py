from common import init_page, predict_from_uploaded_csv, section_card
import plotly.express as px
import streamlit as st

init_page()

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
