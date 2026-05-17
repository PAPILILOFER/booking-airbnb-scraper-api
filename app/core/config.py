from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    MONGO_URL = os.getenv("MONGO_URL")
    MONGO_DB = os.getenv("MONGO_DB")

    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",60)
    )
settings = Settings()
