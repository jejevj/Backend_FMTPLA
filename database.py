import os
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from databases import Database
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the environment variables for the database connection
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct the MySQL connection URL
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the async database object and metadata
database = Database(DATABASE_URL)
metadata = MetaData()

# Define the user_history table with auto-incrementing primary key
user_history = Table(
    "user_history",
    metadata,
    Column("history_id", Integer, primary_key=True, autoincrement=True),  # Auto-incrementing primary key
    Column("access_url", String(255), nullable=False),
    Column("search_query", String(255), nullable=False),
)

# Create an SQLAlchemy engine for migrations and metadata
engine = create_engine(DATABASE_URL)

# Create the table automatically if it doesn't exist (synchronous operation)
# metadata.create_all(engine)
