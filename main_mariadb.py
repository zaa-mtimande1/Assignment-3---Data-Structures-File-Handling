# main_mariadb.py
import pandas as pd
from data_loader import load_articles
from db_loader import insert_article_to_mariadb

# Load CSV
df = load_articles("articles.csv")

# Insert into MariaDB and get IDs
df = df.apply(insert_article_to_mariadb, axis=1)

# Save DataFrame with IDs
df.to_csv("articles_with_mariadb_ids.csv", index=False)
print(df)
