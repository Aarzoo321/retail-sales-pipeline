import pandas as pd

file_path = "data/raw/online_retail_II.xlsx"

# Display sheet names
excel_file = pd.ExcelFile(file_path)

print("Sheet names:")
print(excel_file.sheet_names)

# Read both sheets
for sheet in excel_file.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)

    print(f"\nSheet: {sheet}")
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())