USE retail_sales_db;

-- Remove previous fact records to prevent duplicate loading
TRUNCATE TABLE fact_sales;

-- Populate fact table by connecting staging data
-- with dimension tables

INSERT INTO fact_sales (
    Invoice,
    customer_key,
    product_key,
    country_key,
    date_key,
    Quantity,
    Price,
    Revenue
)
SELECT
    s.Invoice,
    c.customer_key,
    p.product_key,
    co.country_key,
    d.date_key,
    s.Quantity,
    s.Price,
    s.Revenue
FROM staging_retail_sales s

LEFT JOIN dim_customer c
    ON s.CustomerID = c.CustomerID

LEFT JOIN dim_product p
    ON s.StockCode = p.StockCode

LEFT JOIN dim_country co
    ON s.Country = co.Country

LEFT JOIN dim_date d
    ON DATE(s.InvoiceDate) = d.FullDate;


-- Verify fact table
SELECT COUNT(*) AS total_fact_records
FROM fact_sales;

-- Check sample records
SELECT *
FROM fact_sales
LIMIT 10;

-- Calculate total revenue
SELECT SUM(Revenue) AS total_revenue
FROM fact_sales;