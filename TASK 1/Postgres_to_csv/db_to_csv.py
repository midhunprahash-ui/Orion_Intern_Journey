import psycopg2
import pandas as pd
import os

# === Configuration ===
DB_NAME = "my_db"
DB_USER = "postgres"
DB_PASS = "your_password_here"
DB_HOST = "localhost"
DB_PORT = "5432"

SQL_FILE_PATH = "postgres_input_data.sql"
TABLE_NAME = "midhun"
CSV_OUTPUT_PATH = "output.csv"

# === Connect to PostgreSQL ===
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Connected to database.")
except Exception as e:
    print("Database connection failed:", e)
    exit()

cur = conn.cursor()

# === Load SQL file ===
try:
    with open('postgres_input_data.sql', 'r') as f:
        sql_commands = f.read()
    cur.execute(sql_commands)
    conn.commit()
    print(f"Executed SQL from {SQL_FILE_PATH}")
except Exception as e:
    print("SQL execution failed:", e)
    conn.rollback()
    conn.close()
    exit()

# === Export table to CSV ===
try:
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
    df.to_csv(CSV_OUTPUT_PATH, index=False)
    print(f"Exported {TABLE_NAME} to {CSV_OUTPUT_PATH}")
except Exception as e:
    print("CSV export failed:", e)

cur.close()
conn.close()