import pandas as pd
from sqlalchemy import create_engine
import logging

def transform_data(conn_params):
    # Build the SQLAlchemy connection URL
    engine_url = (
        f"postgresql+psycopg2://{conn_params['user']}:{conn_params['password']}"
        f"@{conn_params['host']}:{conn_params['port']}/{conn_params['dbname']}"
    )

    # Create SQLAlchemy engine
    engine = create_engine(engine_url)

    # Define transformation query
    query = """
    SELECT
        p.id AS "postId",
        p.title AS "postTitle",
        p.body AS "postBody",
        u.name AS "userName",
        u.email AS "userEmail"
    FROM staging_posts p
    JOIN staging_users u ON p.userId = u.id
    """

    # Execute the query through SQLAlchemy
    df = pd.read_sql_query(query, engine)
    logging.info("Transformed data and created DataFrame with columns: %s", df.columns.tolist())

    return df