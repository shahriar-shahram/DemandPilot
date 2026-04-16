import pandas as pd

# Load Excel file
df = pd.read_excel("data/raw/walmart_Retail_Data.xlsx")

print("Original shape:", df.shape)
print("Columns:", df.columns)

# Clean column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Convert date column (if exists)
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])

# Sort by date
if "date" in df.columns:
    df = df.sort_values("date")

# Handle missing values
df = df.fillna(0)

# Remove duplicates
df = df.drop_duplicates()

print("Cleaned shape:", df.shape)

# Save cleaned data
df.to_csv("data/processed/clean_data.csv", index=False)

# ===============================
# 🔥 NEW PART: Create time-series
# ===============================

# Aggregate daily sales
daily_sales = df.groupby("order_date")["sales"].sum().reset_index()

print("\nDaily sales preview:")
print(daily_sales.head())

# Save aggregated data
daily_sales.to_csv("data/processed/daily_sales.csv", index=False)