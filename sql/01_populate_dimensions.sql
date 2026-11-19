USE retail_sales_db;

-- ==========================================
-- 1. POPULATE CUSTOMER DIMENSION
-- ==========================================

INSERT INTO dim_customer (CustomerID)
SELECT DISTINCT CustomerID
FROM staging_retail_sales
WHERE CustomerID IS NOT NULL;


-- ==========================================
-- 2. POPULATE PRODUCT DIMENSION
-- ==========================================

INSERT INTO dim_product (StockCode, Description)
SELECT
    StockCode,
    MAX(Description)
FROM staging_retail_sales
GROUP BY StockCode;


-- ==========================================
-- 3. POPULATE DATE DIMENSION
-- ==========================================

INSERT INTO dim_date (date_key, FullDate, Year, Month, Day)
SELECT DISTINCT
    CAST(DATE_FORMAT(InvoiceDate, '%Y%m%d') AS UNSIGNED),
    DATE(InvoiceDate),
    YEAR(InvoiceDate),
    MONTH(InvoiceDate),
    DAY(InvoiceDate)
FROM staging_retail_sales
WHERE InvoiceDate IS NOT NULL;


-- ==========================================
-- 4. POPULATE COUNTRY DIMENSION
-- ==========================================

INSERT INTO dim_country (Country, CountryName, Region)
SELECT DISTINCT
    s.Country,
    s.Country,
    'Unknown'
FROM staging_retail_sales s
WHERE s.Country IS NOT NULL;


-- ==========================================
-- 5. CHECK DIMENSION COUNTS
-- ==========================================

SELECT COUNT(*) AS total_customers FROM dim_customer;

SELECT COUNT(*) AS total_products FROM dim_product;

SELECT COUNT(*) AS total_dates FROM dim_date;

SELECT COUNT(*) AS total_countries FROM dim_country;