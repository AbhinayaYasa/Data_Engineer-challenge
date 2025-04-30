**Junior Data Engineer ETL Project**

**Overview**

This project implements a complete ETL (Extract, Transform, Load) data pipeline that:
Extracts JSON data from a public API (JSONPlaceholder)
Loads raw data into a PostgreSQL database as staging tables
Transforms the data by joining users and posts
Loads the transformed data into a Microsoft SQL Server database (data warehouse)
All components run in Docker containers and are orchestrated using Docker Compose.

**Tech Stack**

- Python 3

- Docker + Docker Compose

- PostgreSQL (staging)

- Microsoft SQL Server (warehouse)

- Libraries: requests, pandas, psycopg2-binary, pyodbc, sqlalchemy, python-dotenv
  
**Setup Instructions:**
python3 -m venv venv - create virtual environment

source venv/bin/activate - activate virtual environment

pip install -r requirements.txt - install dependencies

docker-compose up -d - start docker

**Run ETL Pipeline:** 
python main.py


**For SQL Server:**
sqlcmd -S 127.0.0.1 -U sa -P 'Mypassword@123' -d master

**Then inside sqlcmd:**
USE warehouse_db;
GO

SELECT name from sys.tables;
GO

SELECT TOP 10 * FROM FactUserPosts;


