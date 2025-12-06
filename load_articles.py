import pandas as pd
import mysql.connector
from mysql.connector import Error

# MariaDB connection configuration
MARIADB_CONFIG = {
    "host": "localhost",
    "user": "zaa",
    "password": "Python",
    "database": "python_assignment",
    "port": 3306
}

# Read CSV into pandas DataFrame
df = pd.read_csv("articles.csv", dtype=str)

# Replace NaN values with empty string to avoid SQL errors
df = df.fillna('')

print(f"Loaded {len(df)} rows from articles.csv")

# Function to insert one row into MariaDB


def insert_article(row):
    try:
        conn = mysql.connector.connect(**MARIADB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO articles 
            (title, author, abstract, year, journal, url, pdf_link, arxiv_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['title'],
            row['author'],
            row['abstract'],
            row['year'],
            row['journal'],
            row['url'],
            row['pdf_link'],
            row['arxiv_id']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error inserting row: {e}")
        return False


# Apply the insert function row-wise
df['inserted'] = df.apply(insert_article, axis=1)

print(df)
