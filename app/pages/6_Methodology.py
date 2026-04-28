from common import init_page, section_card
import streamlit as st

init_page()

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
