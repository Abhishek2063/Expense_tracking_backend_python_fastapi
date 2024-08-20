import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    """
    A class to manage application settings based on environment variables.
    """

    # Retrieve the environment type (default to 'local' if not set)
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

    # Determine URLs and database configuration based on the environment
    if ENVIRONMENT == "production":
        API_URL: str = os.getenv("PROD_API_URL")
        APP_URL: str = os.getenv("PROD_APP_URL")
        DATABASE_URL: str = os.getenv("PROD_DATABASE_URL")
    else:
        API_URL: str = os.getenv("LOCAL_API_URL")
        APP_URL: str = os.getenv("LOCAL_APP_URL")
        DATABASE_URL: str = os.getenv("LOCAL_DATABASE_URL")

    # Common settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Instantiate settings
settings = Settings()
