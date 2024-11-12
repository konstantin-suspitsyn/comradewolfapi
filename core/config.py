import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME:str = os.getenv("PROJECT_NAME")

    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT") # default postgres port is 5432
    POSTGRES_DATABASE : str = os.getenv("POSTGRES_DATABASE")
    DATABASE_URL = (f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/"
                    f"{POSTGRES_DATABASE}")

    # If result contains more
    QUERY_ROW_LIMIT = 5_000_000
    ROWS_PER_PAGE = 100_000

settings = Settings()