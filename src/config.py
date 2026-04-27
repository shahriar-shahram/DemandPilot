from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
PREDICTIONS_DIR = DATA_DIR / "predictions"

REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_DIR = REPORTS_DIR / "metrics"

MODELS_DIR = ROOT_DIR / "models"

CLEAN_DATA_PATH = PROCESSED_DIR / "clean_data.csv"
FEATURE_DATA_PATH = PROCESSED_DIR / "forecast_features.csv"

BASELINE_METRICS_PATH = METRICS_DIR / "baseline_metrics.csv"
BASELINE_PREDICTIONS_PATH = PREDICTIONS_DIR / "baseline_predictions.csv"

MODEL_METRICS_PATH = METRICS_DIR / "model_comparison.csv"
PREDICTIONS_PATH = PREDICTIONS_DIR / "forecast_predictions.csv"

BEST_MODEL_PATH = MODELS_DIR / "best_demand_model.joblib"
