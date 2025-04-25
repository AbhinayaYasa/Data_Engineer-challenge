import logging
from etl.extract import fetch_data, USERS_API, POSTS_API
from etl.load_postgres import load_to_postgres
from etl.transform import transform_data
from etl.load_sqlserver import load_to_sqlserver
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)

pg_conn_params = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

sqlserver_conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('SQLSERVER_HOST')},{os.getenv('SQLSERVER_PORT')};"
    f"DATABASE={os.getenv('SQLSERVER_DB')};"
    f"UID={os.getenv('SQLSERVER_USER')};"
    f"PWD={os.getenv('SQLSERVER_PASSWORD')}"
)

def run_pipeline():
    users = fetch_data(USERS_API)
    posts = fetch_data(POSTS_API)
    load_to_postgres(users, "staging_users", pg_conn_params)
    load_to_postgres(posts, "staging_posts", pg_conn_params)
    df = transform_data(pg_conn_params)
    load_to_sqlserver(df, sqlserver_conn_str)

if __name__ == "__main__":
    run_pipeline()
