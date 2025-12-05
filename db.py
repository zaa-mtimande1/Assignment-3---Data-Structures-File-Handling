from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLAlchemy connection string
DB_USER = "example_user"
DB_PASSWORD = "example_pw"
DB_HOST = "127.0.0.1"
DB_PORT = "3307"
DB_NAME = "example_db"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=True  # Set True to see SQL queries printed
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Declarative base for ORM models
Base = declarative_base()