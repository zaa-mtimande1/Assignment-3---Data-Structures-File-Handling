import mysql.connector

MARIADB_CONFIG = {
    "host": "localhost",
    "user": "zaa",
    "password": "Python",
    "database": "python_assignment",
    "port": 3306
}

conn = mysql.connector.connect(**MARIADB_CONFIG)
cursor = conn.cursor()

# Create table for articles
cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    authors VARCHAR(255),
    abstract TEXT,
    publication_date DATE,
    arxiv_id VARCHAR(50)
);
""")

conn.commit()
cursor.close()
conn.close()

print("Articles table created successfully!")
