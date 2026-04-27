import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from config import (
    BEST_MODEL_PATH,
    FEATURE_DATA_PATH,
    METRICS_DIR,
    MODEL_METRICS_PATH,
    MODELS_DIR,
    PREDICTIONS_DIR,
    PREDICTIONS_PATH,
)


CATEGORICAL_FEATURES = ["Region", "Category"]

NUMERIC_FEATURES = [
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


def smape(y_true, y_pred):
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2
    return np.mean(
        np.where(denominator == 0, 0, np.abs(y_true - y_pred) / denominator)
    ) * 100


def wape(y_true, y_pred):
    return np.sum(np.abs(y_true - y_pred)) / np.sum(np.abs(y_true)) * 100


def bias(y_true, y_pred):
    return np.sum(y_pred - y_true) / np.sum(y_true) * 100


def make_pipeline(model):
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", "passthrough", NUMERIC_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def evaluate_predictions(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "SMAPE": smape(y_true, y_pred),
        "WAPE": wape(y_true, y_pred),
        "Bias": bias(y_true, y_pred),
    }


def main():
    df = pd.read_csv(FEATURE_DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    target = "total_sales"
    feature_cols = CATEGORICAL_FEATURES + NUMERIC_FEATURES

    missing_features = [col for col in feature_cols if col not in df.columns]
    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}. Available columns: {list(df.columns)}"
        )

    X = df[feature_cols]
    y = df[target]

    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=250,
            random_state=42,
            n_jobs=-1,
            min_samples_leaf=3,
        ),
        "HistGradientBoosting": HistGradientBoostingRegressor(
            max_iter=300,
            learning_rate=0.05,
            random_state=42,
        ),
    }

    tscv = TimeSeriesSplit(n_splits=5)

    all_metrics = []
    all_predictions = []

    for model_name, model in models.items():
        print(f"\nTraining: {model_name}")
        fold_metrics = []

        for fold, (train_idx, test_idx) in enumerate(tscv.split(X), start=1):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

            pipeline = make_pipeline(model)
            pipeline.fit(X_train, y_train)

            preds = pipeline.predict(X_test)
            metrics = evaluate_predictions(y_test.values, preds)

            metrics["model"] = model_name
            metrics["fold"] = fold
            fold_metrics.append(metrics)

            pred_df = df.iloc[test_idx][
                ["date", "Region", "Category", "total_sales"]
            ].copy()
            pred_df["prediction"] = preds
            pred_df["model"] = model_name
            pred_df["fold"] = fold
            all_predictions.append(pred_df)

        model_metric_df = pd.DataFrame(fold_metrics)
        avg_metrics = (
            model_metric_df.drop(columns=["fold"])
            .groupby("model")
            .mean()
            .reset_index()
        )
        all_metrics.append(avg_metrics)

    metrics_df = pd.concat(all_metrics, ignore_index=True)
    predictions_df = pd.concat(all_predictions, ignore_index=True)

    metrics_df = metrics_df.sort_values("SMAPE")

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(MODEL_METRICS_PATH, index=False)
    predictions_df.to_csv(PREDICTIONS_PATH, index=False)

    best_model_name = metrics_df.iloc[0]["model"]
    best_model = models[best_model_name]

    final_pipeline = make_pipeline(best_model)
    final_pipeline.fit(X, y)

    joblib.dump(final_pipeline, BEST_MODEL_PATH)

    print("\nModel comparison:")
    print(metrics_df)
    print(f"\nBest model saved: {best_model_name}")
    print(f"Model path: {BEST_MODEL_PATH}")


if __name__ == "__main__":
    main()
