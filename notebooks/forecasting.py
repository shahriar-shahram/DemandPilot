import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =========================
# Load category-level dataset
# =========================
df = pd.read_csv("data/processed/daily_category.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df = df.sort_values(["product_category", "order_date"]).reset_index(drop=True)

print("Original shape:", df.shape)
print(df.head())

all_forecasts = []
all_metrics = []

categories = sorted(df["product_category"].dropna().unique())

for category in categories:
    print(f"\nProcessing category: {category}")

    cat_df = df[df["product_category"] == category].copy()
    cat_df = cat_df.sort_values("order_date").reset_index(drop=True)

    # -------------------------
    # Lagged target features
    # -------------------------
    cat_df["lag_1"] = cat_df["total_sales"].shift(1)
    cat_df["lag_7"] = cat_df["total_sales"].shift(7)
    cat_df["lag_14"] = cat_df["total_sales"].shift(14)

    cat_df["rolling_mean_7"] = cat_df["total_sales"].shift(1).rolling(7).mean()
    cat_df["rolling_mean_14"] = cat_df["total_sales"].shift(1).rolling(14).mean()

    # -------------------------
    # Lagged exogenous features
    # -------------------------
    cat_df["avg_discount_lag_1"] = cat_df["avg_discount"].shift(1)
    cat_df["num_orders_lag_1"] = cat_df["num_orders"].shift(1)
    cat_df["total_profit_lag_1"] = cat_df["total_profit"].shift(1)

    # -------------------------
    # Calendar features
    # -------------------------
    cat_df["day_of_week"] = cat_df["order_date"].dt.dayofweek
    cat_df["month"] = cat_df["order_date"].dt.month

    # Drop NaNs from lagging/rolling
    cat_model = cat_df.dropna().reset_index(drop=True)

    print(f"Model-ready rows for {category}: {len(cat_model)}")

    if len(cat_model) < 60:
        print(f"Skipping {category} because it has too few usable rows.")
        continue

    # -------------------------
    # Train/test split
    # -------------------------
    split_idx = int(len(cat_model) * 0.8)
    train = cat_model.iloc[:split_idx].copy()
    test = cat_model.iloc[split_idx:].copy()

    feature_cols = [
        "lag_1",
        "lag_7",
        "lag_14",
        "rolling_mean_7",
        "rolling_mean_14",
        "avg_discount_lag_1",
        "num_orders_lag_1",
        "total_profit_lag_1",
        "day_of_week",
        "month",
    ]

    X_train = train[feature_cols]
    y_train = train["total_sales"]

    X_test = test[feature_cols]
    y_test = test["total_sales"]

    # -------------------------
    # Model
    # -------------------------
    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    model.fit(X_train, y_train)

    test["prediction"] = model.predict(X_test)
    test["prediction"] = test["prediction"].clip(lower=0)

    # -------------------------
    # Metrics
    # -------------------------
    mae = mean_absolute_error(y_test, test["prediction"])
    rmse = np.sqrt(mean_squared_error(y_test, test["prediction"]))

    threshold = 1000
    mask = y_test > threshold

    if mask.sum() > 0:
        smape = (
            np.abs(test.loc[mask, "prediction"] - y_test[mask]) /
            ((np.abs(y_test[mask]) + np.abs(test.loc[mask, "prediction"])) / 2)
        ).mean() * 100
    else:
        smape = np.nan

    weights = y_test / y_test.sum()
    weighted_smape = (
        weights * np.abs(test["prediction"] - y_test) /
        ((np.abs(y_test) + np.abs(test["prediction"])) / 2)
    ).sum() * 100

    print(
        f"{category} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, "
        f"SMAPE: {smape:.2f}%, Weighted SMAPE: {weighted_smape:.2f}%"
    )

    all_metrics.append({
        "product_category": category,
        "train_size": len(train),
        "test_size": len(test),
        "MAE": mae,
        "RMSE": rmse,
        "SMAPE": smape,
        "weighted_SMAPE": weighted_smape,
    })

    forecast_part = test[["order_date", "product_category", "total_sales", "prediction"]].copy()
    all_forecasts.append(forecast_part)

# =========================
# Save combined results
# =========================
if not all_forecasts:
    raise ValueError("No category forecasts were created. Check your input data.")

forecast_df = pd.concat(all_forecasts, ignore_index=True)
metrics_df = pd.DataFrame(all_metrics)

forecast_df.to_csv("data/processed/forecast_results_by_category.csv", index=False)
metrics_df.to_csv("data/processed/forecast_metrics_by_category.csv", index=False)

print("\nAverage metrics across categories:")
print(metrics_df[["MAE", "RMSE", "SMAPE", "weighted_SMAPE"]].mean())

# =========================
# Save plots
# =========================
for category in forecast_df["product_category"].unique():
    plot_df = forecast_df[forecast_df["product_category"] == category].copy()

    plt.figure(figsize=(10, 4))
    plt.plot(plot_df["order_date"], plot_df["total_sales"], label="Actual")
    plt.plot(plot_df["order_date"], plot_df["prediction"], label="Forecast")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.title(f"Category Forecast: {category}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    safe_name = str(category).replace(" ", "_").replace("/", "_")
    plt.savefig(f"data/processed/forecast_plot_category_{safe_name}.png")
    plt.close()

print("\nSaved:")
print("- data/processed/forecast_results_by_category.csv")
print("- data/processed/forecast_metrics_by_category.csv")
print("- forecast_plot_category_<category>.png files")