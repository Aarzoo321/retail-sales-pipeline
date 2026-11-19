
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

# Locate the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the project's .env file
load_dotenv(BASE_DIR / ".env")

# Read database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Create MySQL connection URL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Function to test the connection
def test_db_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()
