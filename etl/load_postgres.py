import psycopg2
import logging

def load_to_postgres(data, table, conn_params):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    if table == "staging_users":
        cur.execute("""CREATE TABLE IF NOT EXISTS staging_users (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            username VARCHAR,
            email VARCHAR
        )""")
        for user in data:
            cur.execute("""INSERT INTO staging_users (id, name, username, email)
                           VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
                        (user['id'], user['name'], user['username'], user['email']))

    elif table == "staging_posts":
        cur.execute("""CREATE TABLE IF NOT EXISTS staging_posts (
            id INTEGER PRIMARY KEY,
            userId INTEGER,
            title TEXT,
            body TEXT
        )""")
        for post in data:
            cur.execute("""INSERT INTO staging_posts (id, userId, title, body)
                           VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
                        (post['id'], post['userId'], post['title'], post['body']))

    conn.commit()
    cur.close()
    conn.close()
    logging.info(f"Loaded data into {table}")