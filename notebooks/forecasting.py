import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =========================
# Load region-level dataset
# =========================
df = pd.read_csv("data/processed/daily_region.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df = df.sort_values(["region", "order_date"]).reset_index(drop=True)

print("Original shape:", df.shape)
print(df.head())

all_forecasts = []
all_metrics = []

regions = sorted(df["region"].dropna().unique())

for region in regions:
    print(f"\nProcessing region: {region}")

    region_df = df[df["region"] == region].copy()
    region_df = region_df.sort_values("order_date").reset_index(drop=True)

    # -------------------------
    # Lagged target features
    # -------------------------
    region_df["lag_1"] = region_df["total_sales"].shift(1)
    region_df["lag_7"] = region_df["total_sales"].shift(7)
    region_df["lag_14"] = region_df["total_sales"].shift(14)

    region_df["rolling_mean_7"] = region_df["total_sales"].shift(1).rolling(7).mean()
    region_df["rolling_mean_14"] = region_df["total_sales"].shift(1).rolling(14).mean()

    # -------------------------
    # Lagged exogenous features
    # -------------------------
    region_df["avg_discount_lag_1"] = region_df["avg_discount"].shift(1)
    region_df["num_orders_lag_1"] = region_df["num_orders"].shift(1)
    region_df["total_profit_lag_1"] = region_df["total_profit"].shift(1)

    # -------------------------
    # Calendar features
    # -------------------------
    region_df["day_of_week"] = region_df["order_date"].dt.dayofweek
    region_df["month"] = region_df["order_date"].dt.month

    # Drop NaNs from lagging/rolling
    region_model = region_df.dropna().reset_index(drop=True)

    print(f"Model-ready rows for {region}: {len(region_model)}")

    # Skip tiny regions if needed
    if len(region_model) < 60:
        print(f"Skipping {region} because it has too few usable rows.")
        continue

    # -------------------------
    # Train/test split
    # -------------------------
    split_idx = int(len(region_model) * 0.8)
    train = region_model.iloc[:split_idx].copy()
    test = region_model.iloc[split_idx:].copy()

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
    model = LinearRegression()
    model.fit(X_train, y_train)

    test["prediction"] = model.predict(X_test)
    test["prediction"] = test["prediction"].clip(lower=0)

    # -------------------------
    # Metrics
    # -------------------------
    mae = mean_absolute_error(y_test, test["prediction"])
    rmse = np.sqrt(mean_squared_error(y_test, test["prediction"]))

    threshold = 1000  # adjust based on your data

    mask = y_test > threshold

    smape = (
                    np.abs(test.loc[mask, "prediction"] - y_test[mask]) /
                    ((np.abs(y_test[mask]) + np.abs(test.loc[mask, "prediction"])) / 2)
            ).mean() * 100

    print(f"{region} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, SMAPE: {smape:.2f}%")

    all_metrics.append({
        "region": region,
        "train_size": len(train),
        "test_size": len(test),
        "MAE": mae,
        "RMSE": rmse,
        "SMAPE": smape,
    })

    weights = y_test / y_test.sum()

    weighted_smape = (
                             weights * np.abs(test["prediction"] - y_test) /
                             ((np.abs(y_test) + np.abs(test["prediction"])) / 2)
                     ).sum() * 100

    print(f"Weighted SMAPE: {weighted_smape:.2f}%")

    forecast_part = test[["order_date", "region", "total_sales", "prediction"]].copy()
    all_forecasts.append(forecast_part)

# =========================
# Save combined results
# =========================
if not all_forecasts:
    raise ValueError("No regional forecasts were created. Check your input data.")

forecast_df = pd.concat(all_forecasts, ignore_index=True)
metrics_df = pd.DataFrame(all_metrics)

forecast_df.to_csv("data/processed/forecast_results_by_region.csv", index=False)
metrics_df.to_csv("data/processed/forecast_metrics_by_region.csv", index=False)

print("\nAverage metrics across regions:")
print(metrics_df[["MAE", "RMSE", "SMAPE"]].mean())

# =========================
# Optional overall plot
# =========================
for region in forecast_df["region"].unique():
    plot_df = forecast_df[forecast_df["region"] == region].copy()

    plt.figure(figsize=(10, 4))
    plt.plot(plot_df["order_date"], plot_df["total_sales"], label="Actual")
    plt.plot(plot_df["order_date"], plot_df["prediction"], label="Forecast")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.title(f"Regional Forecast: {region}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"data/processed/forecast_plot_{region}.png")
    plt.close()

print("\nSaved:")
print("- data/processed/forecast_results_by_region.csv")
print("- data/processed/forecast_metrics_by_region.csv")
print("- forecast_plot_<region>.png files")