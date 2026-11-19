import pandas as pd

files = {
    "Country Region": "data/reference/country_region.csv",
    "Exchange Rates": "data/reference/fx_rates_gbp_usd.csv",
    "Non Product Codes": "data/reference/non_product_codes.csv"
}

for name, file_path in files.items():

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    df = pd.read_csv(file_path)

    print("Columns:", df.columns.tolist())
    print("Rows:", len(df))

    print("\nData:")
    print(df.head(10).to_string(index=False))