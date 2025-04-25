import pyodbc
import logging

def load_to_sqlserver(df, conn_str):
    try:
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()

        # ensure the target database exists
        cursor.execute("IF DB_ID('warehouse_db') IS NULL CREATE DATABASE warehouse_db")
        cursor.execute("USE warehouse_db")

        # creates the table if it doesn't exist
        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='FactUserPosts' AND xtype='U')
        CREATE TABLE FactUserPosts (
            postId INT PRIMARY KEY,
            postTitle NVARCHAR(MAX),
            postBody NVARCHAR(MAX),
            userName NVARCHAR(255),
            userEmail NVARCHAR(255)
        )
        """)
        conn.commit()
        print("📊 DataFrame columns:", df.columns.tolist())

        # insert data using MERGE
        for _, row in df.iterrows():
            cursor.execute("""
            MERGE INTO FactUserPosts AS target
            USING (SELECT ? AS postId) AS source
            ON target.postId = source.postId
            WHEN NOT MATCHED THEN
                INSERT (postId, postTitle, postBody, userName, userEmail)
                VALUES (?, ?, ?, ?, ?);
            """, row['postId'], row['postId'], row['postTitle'], row['postBody'], row['userName'], row['userEmail'])

        conn.commit()
        cursor.close()
        conn.close()

        logging.info("Loaded transformed data into SQL Server.")

    except pyodbc.Error as e:
        logging.error(f"pyodbc error while inserting to SQL Server: {e}")
    except Exception as e:
        logging.error(f"General error: {e}")
