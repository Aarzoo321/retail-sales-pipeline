import pandas as pd

file_path = "data/processed/cleaned_data.csv"

df = pd.read_csv(file_path, dtype={"Invoice": str}, low_memory=False)

print("CLEANED DATA VALIDATION")
print("=" * 40)

print("Total rows:", len(df))
print("Duplicate rows:", df.duplicated().sum())

print("\nMissing values:")
print(df.isnull().sum())

print("\nInvalid prices:", (df["Price"] <= 0).sum())

print("\nCancelled invoices:",
      df["Invoice"].astype(str).str.startswith("C").sum())

print("\nRevenue calculation check:")
print((df["Revenue"] == df["Quantity"] * df["Price"]).all())

print("\nDate range:")
print(df["InvoiceDate"].min())
print(df["InvoiceDate"].max())

print("\nValidation completed!")