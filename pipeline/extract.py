import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input Excel file
INPUT_FILE = BASE_DIR / "data" / "raw" / "online_retail_II.xlsx"

# Output directory
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Read both Excel sheets
sheets = pd.read_excel(INPUT_FILE, sheet_name=None)

# Combine both sheets into one DataFrame
dataframes = []

for sheet_name, df in sheets.items():
    df["source_sheet"] = sheet_name
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# Save extracted data
output_file = OUTPUT_DIR / "extracted_data.csv"

combined_df.to_csv(output_file, index=False)

print("Extraction completed successfully!")
print("Total rows:", len(combined_df))
print("Columns:", combined_df.columns.tolist())
print("Saved file:", output_file)