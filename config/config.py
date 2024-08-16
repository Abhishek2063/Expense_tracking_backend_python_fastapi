import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ENVIORNMENT: str = os.getenv("ENVIORNMENT", "local")

    if ENVIORNMENT == "production":
        API_URL: str = os.getenv("PROD_API_URL")
        APP_URL: str = os.getenv("PROD_APP_URL")
        DATABASE_URL: str = os.getenv("PROD_DATABASE_URL")
    else:
        API_URL: str = os.getenv("LOCAL_API_URL")
        APP_URL: str = os.getenv("LOCAL_APP_URL")
        DATABASE_URL: str = os.getenv("LOCAL_DATABASE_URL")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
