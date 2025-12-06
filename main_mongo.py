# main_mongo.py
import pandas as pd
from mongo_loader import insert_article_to_mongo

# Load DataFrame with MariaDB IDs and/or ArXiv data
df = pd.read_csv("arxiv_articles_with_html.csv", dtype=str)

# If you already have MariaDB IDs, merge them into this DF
# df = df.merge(df_mariadb[['title','mariadb_id']], on='title', how='left')

# Insert into MongoDB
df = df.apply(insert_article_to_mongo, axis=1)
print("Inserted all articles into MongoDB.")
