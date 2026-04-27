import numpy as np
import pandas as pd

from config import (
    BASELINE_METRICS_PATH,
    BASELINE_PREDICTIONS_PATH,
    FEATURE_DATA_PATH,
    METRICS_DIR,
    PREDICTIONS_DIR,
)


def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def smape(y_true, y_pred):
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2
    return np.mean(
        np.where(denominator == 0, 0, np.abs(y_true - y_pred) / denominator)
    ) * 100


def wape(y_true, y_pred):
    return np.sum(np.abs(y_true - y_pred)) / np.sum(np.abs(y_true)) * 100


def bias(y_true, y_pred):
    return np.sum(y_pred - y_true) / np.sum(y_true) * 100


def evaluate_model(name, df, prediction_col):
    y_true = df["total_sales"].values
    y_pred = df[prediction_col].values

    return {
        "model": name,
        "MAE": mae(y_true, y_pred),
        "RMSE": rmse(y_true, y_pred),
        "SMAPE": smape(y_true, y_pred),
        "WAPE": wape(y_true, y_pred),
        "Bias": bias(y_true, y_pred),
    }


def main():
    df = pd.read_csv(FEATURE_DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["Region", "Category", "date"])

    df["naive_lag_1"] = df["sales_lag_1"]
    df["seasonal_naive_lag_7"] = df["sales_lag_7"]
    df["rolling_mean_7"] = df["sales_roll_mean_7"]

    baseline_df = df.dropna(
        subset=["naive_lag_1", "seasonal_naive_lag_7", "rolling_mean_7"]
    ).copy()

    metrics = [
        evaluate_model("Naive Lag-1", baseline_df, "naive_lag_1"),
        evaluate_model("Seasonal Naive Lag-7", baseline_df, "seasonal_naive_lag_7"),
        evaluate_model("Rolling Mean-7", baseline_df, "rolling_mean_7"),
    ]

    metrics_df = pd.DataFrame(metrics).sort_values("SMAPE")

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(BASELINE_METRICS_PATH, index=False)
    baseline_df.to_csv(BASELINE_PREDICTIONS_PATH, index=False)

    print("Baseline model comparison:")
    print(metrics_df)


if __name__ == "__main__":
    main()
