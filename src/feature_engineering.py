import pandas as pd

from config import CLEAN_DATA_PATH, FEATURE_DATA_PATH, PROCESSED_DIR


REQUIRED_COLUMNS = [
    "order_date",
    "region",
    "product_category",
    "sales",
    "profit",
    "discount",
    "order_id",
    "order_quantity",
    "product_name",
]


def load_clean_data(path=CLEAN_DATA_PATH):
    df = pd.read_csv(path)

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Missing required columns: {missing_cols}. "
            f"Available columns: {list(df.columns)}"
        )

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


def build_daily_panel(df):
    group_cols = ["date", "Region", "Category"]

    daily = (
        df.groupby(group_cols)
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum"),
            avg_discount=("Discount", "mean"),
            num_orders=("Order ID", "nunique"),
            unique_products=("Product Name", "nunique"),
            avg_quantity=("Quantity", "mean"),
            shipping_cost=("shipping_cost", "mean"),
            avg_unit_price=("unit_price", "mean"),
            avg_product_margin=("product_base_margin", "mean"),
        )
        .reset_index()
        .sort_values(["Region", "Category", "date"])
    )

    return daily


def add_time_features(df):
    df = df.copy()

    df["day_of_week"] = df["date"].dt.dayofweek
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    return df


def add_lag_features(df):
    df = df.copy()
    group_cols = ["Region", "Category"]

    for lag in [1, 7, 14, 28]:
        df[f"sales_lag_{lag}"] = df.groupby(group_cols)["total_sales"].shift(lag)

    for window in [7, 14, 28]:
        shifted_sales = df.groupby(group_cols)["total_sales"].shift(1)

        df[f"sales_roll_mean_{window}"] = (
            shifted_sales.groupby([df["Region"], df["Category"]])
            .rolling(window)
            .mean()
            .reset_index(level=[0, 1], drop=True)
        )

        df[f"sales_roll_std_{window}"] = (
            shifted_sales.groupby([df["Region"], df["Category"]])
            .rolling(window)
            .std()
            .reset_index(level=[0, 1], drop=True)
        )

    df["discount_lag_1"] = df.groupby(group_cols)["avg_discount"].shift(1)
    df["profit_lag_1"] = df.groupby(group_cols)["total_profit"].shift(1)
    df["orders_lag_1"] = df.groupby(group_cols)["num_orders"].shift(1)
    df["shipping_cost_lag_1"] = df.groupby(group_cols)["shipping_cost"].shift(1)
    df["unit_price_lag_1"] = df.groupby(group_cols)["avg_unit_price"].shift(1)
    df["margin_lag_1"] = df.groupby(group_cols)["avg_product_margin"].shift(1)

    return df


def build_features():
    df = load_clean_data()

    panel = build_daily_panel(df)
    panel = add_time_features(panel)
    panel = add_lag_features(panel)

    panel = panel.dropna().reset_index(drop=True)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(FEATURE_DATA_PATH, index=False)

    print(f"Saved feature table to: {FEATURE_DATA_PATH}")
    print(f"Feature table shape: {panel.shape}")
    print("\nFeature columns:")
    print(panel.columns.tolist())
    print("\nPreview:")
    print(panel.head())


if __name__ == "__main__":
    build_features()
