import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "extracted_data.csv"
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("DATA QUALITY PROFILING")
print("=" * 60)

# 1. Basic information
print("\nTotal rows:", len(df))
print("Total columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

# 2. Data types
print("\nData types:")
print(df.dtypes)

# 3. Missing values
print("\nMissing values:")
print(df.isnull().sum())

# 4. Duplicate records
print("\nDuplicate rows:", df.duplicated().sum())

# 5. Negative quantity
print("\nNegative quantity rows:", (df["Quantity"] < 0).sum())

# 6. Zero quantity
print("Zero quantity rows:", (df["Quantity"] == 0).sum())

# 7. Negative or zero price
print("Zero/negative price rows:", (df["Price"] <= 0).sum())

# 8. Cancelled invoices
cancelled = df["Invoice"].astype(str).str.startswith("C")
print("Cancelled invoice rows:", cancelled.sum())

# 9. Date range
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

print("\nDate range:")
print("Earliest:", df["InvoiceDate"].min())
print("Latest:", df["InvoiceDate"].max())

# 10. Save missing-value report
missing_report = pd.DataFrame({
    "column": df.columns,
    "missing_count": df.isnull().sum().values,
    "missing_percentage": (
        df.isnull().sum().values / len(df) * 100
    ).round(2)
})

missing_report.to_csv(
    OUTPUT_DIR / "missing_values_report.csv",
    index=False
)

print("\nMissing-value report saved.")

# 11. Save profiling summary
summary = {
    "total_rows": len(df),
    "total_columns": len(df.columns),
    "duplicate_rows": int(df.duplicated().sum()),
    "negative_quantity_rows": int((df["Quantity"] < 0).sum()),
    "zero_quantity_rows": int((df["Quantity"] == 0).sum()),
    "zero_or_negative_price_rows": int((df["Price"] <= 0).sum()),
    "cancelled_invoice_rows": int(cancelled.sum()),
    "missing_customer_id": int(df["Customer ID"].isnull().sum()),
    "missing_description": int(df["Description"].isnull().sum()),
    "earliest_date": str(df["InvoiceDate"].min()),
    "latest_date": str(df["InvoiceDate"].max())
}

summary_df = pd.DataFrame(
    list(summary.items()),
    columns=["metric", "value"]
)

summary_df.to_csv(
    OUTPUT_DIR / "data_quality_summary.csv",
    index=False
)

print("\nProfiling completed!")
print("\nSummary:")
print(summary_df.to_string(index=False))
print("\nReports saved inside docs/")