import mysql.connector
from config import MARIADB_CONFIG

try:
    conn = mysql.connector.connect(**MARIADB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Connected! Tables:", tables)
    conn.close()
except mysql.connector.Error as err:
    print("Error:", err)
