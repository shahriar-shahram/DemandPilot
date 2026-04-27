# DemandPilot Forecasting Model Card

## Model Purpose

This model powers the DemandPilot retail demand forecasting workflow. It predicts daily demand at the region-category level using historical sales, profit, discount, product, shipping, margin, and calendar-based features.

## Model Type

The current best model is selected automatically from the training pipeline based on SMAPE. In the current run, the best model is a Random Forest regressor trained through a scikit-learn pipeline with categorical encoding and numerical demand features.

## Input Features

The model expects the engineered feature table produced by:

```bash
python src/feature_engineering.py

Now create the backend inference module:

```bash
cat > src/inference.py <<'EOF'
import joblib
import pandas as pd

from config import BEST_MODEL_PATH
from feature_engineering import add_lag_features, add_time_features, build_daily_panel


REQUIRED_UPLOAD_COLUMNS = [
    "order_date",
    "region",
    "product_category",
    "sales",
    "profit",
    "discount",
    "order_id",
    "order_quantity",
    "product_name",
    "shipping_cost",
    "unit_price",
    "product_base_margin",
]


MODEL_FEATURE_COLUMNS = [
    "Region",
    "Category",
    "total_profit",
    "avg_discount",
    "num_orders",
    "unique_products",
    "avg_quantity",
    "shipping_cost",
    "avg_unit_price",
    "avg_product_margin",
    "day_of_week",
    "week_of_year",
    "month",
    "quarter",
    "is_weekend",
    "sales_lag_1",
    "sales_lag_7",
    "sales_lag_14",
    "sales_lag_28",
    "sales_roll_mean_7",
    "sales_roll_std_7",
    "sales_roll_mean_14",
    "sales_roll_std_14",
    "sales_roll_mean_28",
    "sales_roll_std_28",
    "discount_lag_1",
    "profit_lag_1",
    "orders_lag_1",
    "shipping_cost_lag_1",
    "unit_price_lag_1",
    "margin_lag_1",
]


def load_model(model_path=BEST_MODEL_PATH):
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found at {model_path}. "
            "Run `python src/train_models.py` to train and save the model."
        )

    return joblib.load(model_path)


def validate_uploaded_schema(uploaded_df):
    missing_cols = [
        col for col in REQUIRED_UPLOAD_COLUMNS if col not in uploaded_df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Uploaded file is missing required columns: {missing_cols}. "
            f"Available columns: {list(uploaded_df.columns)}"
        )


def standardize_uploaded_data(uploaded_df):
    validate_uploaded_schema(uploaded_df)

    df = uploaded_df.copy()

    df = df.rename(
        columns={
            "order_date": "date",
            "region": "Region",
            "product_category": "Category",
            "sales": "Sales",
            "profit": "Profit",
            "discount": "Discount",
            "order_id": "Order ID",
            "order_quantity": "Quantity",
            "product_name": "Product Name",
        }
    )

    df["date"] = pd.to_datetime(df["date"])
    return df


def prepare_uploaded_data(uploaded_df):
    df = standardize_uploaded_data(uploaded_df)

    panel = build_daily_panel(df)
    panel = add_time_features(panel)
    panel = add_lag_features(panel)
    panel = panel.dropna().reset_index(drop=True)

    return panel


def predict_from_feature_table(feature_df, model=None):
    if model is None:
        model = load_model()

    missing_features = [
        col for col in MODEL_FEATURE_COLUMNS if col not in feature_df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Feature table is missing required model features: {missing_features}"
        )

    output = feature_df.copy()
    output["forecast_sales"] = model.predict(output[MODEL_FEATURE_COLUMNS])

    return output


def predict_from_uploaded_csv(uploaded_file):
    uploaded_df = pd.read_csv(uploaded_file)
    feature_df = prepare_uploaded_data(uploaded_df)
    model = load_model()
    predictions = predict_from_feature_table(feature_df, model=model)

    return predictions
