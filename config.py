import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "")


def get_engine():
    # Credentials must be URL-encoded -- a password containing @, :, /, or %
    # (e.g. "Monday@123") would otherwise be misparsed as part of the host.
    user = quote_plus(DB_USER)
    password = quote_plus(DB_PASSWORD)
    url = f"postgresql+psycopg2://{user}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)
