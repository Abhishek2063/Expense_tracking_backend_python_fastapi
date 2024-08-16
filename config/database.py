from config.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create schema if it does not exist
with engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS expanse_tracking_python;"))
    connection.commit()

# Configure session factory
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Define the base class for model class definitions
Base = declarative_base()

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()