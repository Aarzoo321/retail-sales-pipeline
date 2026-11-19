# Retail Sales Data Pipeline

## Project Overview
This project builds an ETL pipeline for retail sales data using Python, Pandas, and MySQL. It extracts data from Excel files, cleans and validates it, and loads it into a MySQL database using a dimensional data model.

## Technology Stack
- Python
- Pandas
- MySQL
- FastAPI
- SQLAlchemy
- Pytest

## Pipeline Workflow
1. Extract data from Excel files.
2. Profile the raw data.
3. Clean and transform the data.
4. Validate data quality.
5. Load data into MySQL staging table.
6. Populate dimension tables.
7. Populate fact sales table.
8. Access data through REST APIs.

## Database Schema
- dim_customer
- dim_product
- dim_country
- dim_date
- fact_sales
- staging_retail_sales

## API Endpoints
- GET `/` - API home
- GET `/health` - Health check
- GET `/health/database` - Database health
- GET `/sales/summary` - Sales summary
- GET `/sales/top-products` - Top products

## Run the Project

### Install dependencies
pip install -r requirements.txt

### Run ETL
python pipeline/extract.py
python pipeline/transform.py
python pipeline/validate.py
python pipeline/load.py

### Run API
uvicorn api.main:app --reload

### API Documentation
http://127.0.0.1:8000/docs

### Run Tests
pytest

## Data Quality
The pipeline removes duplicate records, cancelled invoices, invalid prices, missing descriptions, and non-product codes.

## Testing
Automated API tests are implemented using Pytest.