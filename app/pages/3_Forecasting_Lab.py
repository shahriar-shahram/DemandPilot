from common import init_page, load_metrics, load_predictions, section_card
import plotly.express as px
import streamlit as st

init_page()

metrics = load_metrics()

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
