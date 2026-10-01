import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv(encoding='utf-8')
def get_connection():
    return psycopg2.connect(
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        host=os.getenv('host'),
        port=os.getenv('port')
    )
def get_engine():
    db_url=(
        f"postgresql://{os.getenv('user')}:"
        f"{os.getenv('password')}@"
        f"{os.getenv('host')}:"
        f"{os.getenv('port')}/"
        f"{os.getenv('database')}"
    )
    return create_engine(db_url)
