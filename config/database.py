from config.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Retrieve the database URL from application settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine with echo=True to log SQL queries for debugging
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create the database schema if it does not exist
with engine.connect() as connection:
    # Execute SQL to create schema
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS expanse_tracking_python;"))
    # Commit the transaction
    connection.commit()

# Configure the session factory for SQLAlchemy
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Define the base class for model class definitions
Base = declarative_base()

def get_db():
    """
    Dependency to get a database session.

    Yields:
        Session: The SQLAlchemy session object.
    """
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the session for use in FastAPI endpoints
        yield db
    finally:
        # Ensure the session is closed after use
        db.close()
