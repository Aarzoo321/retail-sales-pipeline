from fastapi import FastAPI
from api.database import test_db_connection , engine
from sqlalchemy import text

app = FastAPI(
    title="Retail Sales Data API",
    description="API for accessing retail sales data",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Retail Sales API is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
def database_health():
    try:
        result = test_db_connection()

        return {
            "status": "healthy",
            "database": "connected",
            "test_result": result
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }

@app.get("/sales/summary")
def sales_summary():

    query = text("""
        SELECT
            COUNT(*) AS total_records,
            SUM(Revenue) AS total_revenue,
            SUM(Quantity) AS total_quantity,
            COUNT(DISTINCT customer_key) AS unique_customers,
            COUNT(DISTINCT product_key) AS unique_products
        FROM fact_sales
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        row = result.fetchone()

    return {
        "total_records": row[0],
        "total_revenue": float(row[1]),
        "total_quantity": int(row[2]),
        "unique_customers": row[3],
        "unique_products": row[4]
    }

@app.get("/sales/by-country")
def sales_by_country():
    query = text("""
        SELECT dc.Country, SUM(fs.Revenue) AS revenue
        FROM fact_sales fs
        JOIN dim_country dc ON fs.country_key = dc.country_key
        GROUP BY dc.Country
        ORDER BY revenue DESC
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).fetchall()

    return [{"country": row[0], "revenue": float(row[1])} for row in rows]


@app.get("/sales/by-month")
def sales_by_month():
    query = text("""
        SELECT dd.Year, dd.Month, SUM(fs.Revenue) AS revenue
        FROM fact_sales fs
        JOIN dim_date dd ON fs.date_key = dd.date_key
        GROUP BY dd.Year, dd.Month
        ORDER BY dd.Year, dd.Month
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).fetchall()

    return [
        {"year": row[0], "month": row[1], "revenue": float(row[2])}
        for row in rows
    ]


@app.get("/sales/top-products")
def top_products():
    query = text("""
        SELECT dp.Description, SUM(fs.Quantity) AS quantity,
               SUM(fs.Revenue) AS revenue
        FROM fact_sales fs
        JOIN dim_product dp ON fs.product_key = dp.product_key
        GROUP BY dp.Description
        ORDER BY revenue DESC
        LIMIT 10
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).fetchall()

    return [
        {
            "product": row[0],
            "quantity_sold": int(row[1]),
            "revenue": float(row[2])
        }
        for row in rows
    ]