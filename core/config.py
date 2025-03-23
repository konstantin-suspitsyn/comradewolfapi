import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    PROJECT_HOST: str = os.getenv("PROJECT_HOST")

    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE : str = os.getenv("POSTGRES_DATABASE")
    DATABASE_URL = (f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/"
                    f"{POSTGRES_DATABASE}")

    # If result contains more
    QUERY_ROW_LIMIT = 1_000_000
    ROWS_PER_PAGE = 100_000

    MAX_FILTER_VALUES = 1_000

    # Auth settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    # Expiration time in seconds
    EXPIRE_JWT_IN: int = 24 * 60 * 60
    # Expiration time in seconds
    EXPIRE_CONFIRMATION_CODE: int = 24 * 60 * 60
    #Password expiration time in seconds
    EXPIRE_PASSWORD_RESTORATION_CODE = 24 * 60 * 60

    # All about mail
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")


settings = Settings()
