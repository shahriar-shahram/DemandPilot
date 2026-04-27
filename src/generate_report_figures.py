import pandas as pd
import matplotlib.pyplot as plt

from config import MODEL_METRICS_PATH, PREDICTIONS_PATH, FIGURES_DIR


def save_model_comparison():
    metrics = pd.read_csv(MODEL_METRICS_PATH)

    plt.figure(figsize=(10, 6))
    plt.bar(metrics["model"], metrics["SMAPE"])
    plt.ylabel("SMAPE (%)")
    plt.xlabel("Model")
    plt.title("Demand Forecasting Model Comparison")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURES_DIR / "model_comparison_smape.png", dpi=200)
    plt.close()


def save_forecast_example():
    preds = pd.read_csv(PREDICTIONS_PATH)
    preds["date"] = pd.to_datetime(preds["date"])

    best_model = (
        preds.groupby("model")
        .apply(lambda x: (x["total_sales"] - x["prediction"]).abs().mean())
        .sort_values()
        .index[0]
    )

    example = preds[preds["model"] == best_model].copy()

    segment = (
        example.groupby(["Region", "Category"])["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    region, category = segment

    example = example[
        (example["Region"] == region) & (example["Category"] == category)
    ].sort_values("date")

    plt.figure(figsize=(12, 6))
    plt.plot(example["date"], example["total_sales"], label="Actual Demand")
    plt.plot(example["date"], example["prediction"], label="Forecast")
    plt.title(f"Actual vs Forecast Demand: {region} / {category}")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend()
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / "actual_vs_forecast.png", dpi=200)
    plt.close()


def save_error_over_time():
    preds = pd.read_csv(PREDICTIONS_PATH)
    preds["date"] = pd.to_datetime(preds["date"])
    preds["abs_error"] = (preds["total_sales"] - preds["prediction"]).abs()

    best_model = (
        preds.groupby("model")["abs_error"]
        .mean()
        .sort_values()
        .index[0]
    )

    error_df = (
        preds[preds["model"] == best_model]
        .groupby("date")["abs_error"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))
    plt.plot(error_df["date"], error_df["abs_error"])
    plt.title(f"Forecast Error Over Time: {best_model}")
    plt.xlabel("Date")
    plt.ylabel("Mean Absolute Error")
    plt.tight_layout()

    plt.savefig(FIGURES_DIR / "forecast_error_over_time.png", dpi=200)
    plt.close()


def main():
    save_model_comparison()
    save_forecast_example()
    save_error_over_time()

    print(f"Saved figures to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
