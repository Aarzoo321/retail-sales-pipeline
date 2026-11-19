import pandas as pd
import pymysql
import os
from dotenv import load_dotenv
from pathlib import Path

# --------------------------------------------------
# 1. Project directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# 2. Load environment variables
# --------------------------------------------------

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# 3. CSV file path
# --------------------------------------------------

CSV_FILE = BASE_DIR / "data" / "processed" / "cleaned_data.csv"

# --------------------------------------------------
# 4. Connect to MySQL
# --------------------------------------------------

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("Connected to MySQL successfully!")

# --------------------------------------------------
# 5. SQL INSERT query
# --------------------------------------------------

insert_query = """
INSERT INTO staging_retail_sales (
    Invoice,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    Price,
    CustomerID,
    Country,
    SourceSheet,
    Revenue,
    Year,
    Month,
    Day
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor = None

try:

    cursor = connection.cursor()

    # Clear existing staging data
    cursor.execute("TRUNCATE TABLE staging_retail_sales")

    print("Previous staging data cleared.")

    # Batch size
    chunk_size = 5000

    total_loaded = 0

    # --------------------------------------------------
    # 6. Read CSV in batches
    # --------------------------------------------------

    for chunk in pd.read_csv(
        CSV_FILE,
        chunksize=chunk_size,
        dtype={
            "Invoice": str,
            "StockCode": str
        },
        low_memory=False
    ):

        # Rename columns
        chunk = chunk.rename(columns={
            "Customer ID": "CustomerID",
            "source_sheet": "SourceSheet"
        })

        # --------------------------------------------------
        # 7. Clean Customer IDs
        # --------------------------------------------------

        chunk["CustomerID"] = chunk["CustomerID"].apply(
            lambda value: (
                int(value)
                if pd.notna(value)
                else None
            )
        )

        # --------------------------------------------------
        # 8. Convert all missing values to None
        # --------------------------------------------------

        rows = []

        for row in chunk.itertuples(index=False, name=None):

            cleaned_row = []

            for value in row:

                # Missing values -> SQL NULL
                if pd.isna(value):
                    value = None

                # Convert NumPy data types to Python types
                elif hasattr(value, "item"):
                    value = value.item()

                cleaned_row.append(value)

            rows.append(tuple(cleaned_row))

        # --------------------------------------------------
        # 9. Insert batch into MySQL
        # --------------------------------------------------

        cursor.executemany(insert_query, rows)

        # Save batch
        connection.commit()

        # Update count
        total_loaded += len(rows)

        print(f"Loaded {total_loaded:,} rows...")

    # --------------------------------------------------
    # 10. Success message
    # --------------------------------------------------

    print("\n===================================")
    print("DATA LOADING COMPLETED SUCCESSFULLY")
    print("===================================")
    print(f"Total rows loaded: {total_loaded:,}")

except Exception as error:

    connection.rollback()

    print("\nERROR DURING DATA LOADING")
    print(error)

finally:

    if cursor is not None:
        cursor.close()

    connection.close()

    print("MySQL connection closed.")