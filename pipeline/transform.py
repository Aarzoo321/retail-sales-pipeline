import pandas as pd

# File paths
input_file = "data/processed/extracted_data.csv"
output_file = "data/processed/cleaned_data.csv"
reference_file = "data/reference/non_product_codes.csv"

print("Starting data cleaning...")

# Load extracted data
df = pd.read_csv(input_file)

initial_rows = len(df)

# 1. Remove duplicate rows
df = df.drop_duplicates()

# 2. Remove cancelled invoices
df = df[~df["Invoice"].astype(str).str.startswith("C")]

# 3. Remove rows with missing descriptions
df = df.dropna(subset=["Description"])

# 4. Remove rows with invalid prices
df = df[df["Price"] > 0]

# 5. Remove non-product stock codes
non_products = pd.read_csv(reference_file)

excluded_codes = non_products["stock_code"].astype(str).tolist()

df["StockCode"] = df["StockCode"].astype(str)

df = df[~df["StockCode"].isin(excluded_codes)]

# 6. Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 7. Create calculated column: Revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# 8. Create date-based columns
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Day"] = df["InvoiceDate"].dt.day

# Save cleaned data
df.to_csv(output_file, index=False)

print("\nCleaning completed successfully!")
print("Initial rows:", initial_rows)
print("Final rows:", len(df))
print("Rows removed:", initial_rows - len(df))
print("Final columns:", df.columns.tolist())
print("Saved to:", output_file)