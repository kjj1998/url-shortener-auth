"""Unit of work pattern implementation"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

parent_directory_path = os.path.dirname(os.getcwd())
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)

DB_URL = ""

if os.getenv("PROD") and os.getenv("PROD").lower() == "true":
    url_tokens = {
        "DB_USER": os.getenv("DB_USER"),
        "DB_PW": os.getenv("DB_PW"),
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_PORT": os.getenv("DB_PORT"),
        "REDIS_HOST": os.getenv("REDIS_HOST"),
        "REDIS_PORT": os.getenv("REDIS_PORT"),
    }
else:
    url_tokens = {
        "DB_USER": os.getenv("POSTGRES_DEV_USER"),
        "DB_PW": os.getenv("POSTGRES_DEV_PW"),
        "DB_HOST": os.getenv("POSTGRES_K8s_HOST", os.getenv("POSTGRES_DEV_HOST")),
        "DB_NAME": os.getenv("POSTGRES_DEV_DB"),
        "DB_PORT": os.getenv("POSTGRES_DEV_PORT"),
        "REDIS_HOST": os.getenv("REDIS_K8s_HOST", os.getenv("REDIS_DEV_HOST")),
        "REDIS_PORT": os.getenv("REDIS_DEV_PORT"),
    }

DB_URL = (
    f"postgresql://{url_tokens["DB_USER"]}:{url_tokens["DB_PW"]}@"
    f"{url_tokens["DB_HOST"]}:{url_tokens["DB_PORT"]}/{url_tokens["DB_NAME"]}"
)

assert DB_URL is not None, "DB_URL environment variable needed."


class UnitOfWork:
    """Unit of work pattern implementation"""

    def __init__(self):
        self.session_maker = sessionmaker(bind=create_engine(DB_URL))
        self.session = None

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        """Commit the transaction"""
        self.session.commit()

    def rollback(self):
        """Rollback the transaction"""
        self.session.rollback()
