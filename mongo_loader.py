# mongo_loader.py
import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "python_assignment"
COLLECTION_NAME = "articles"


def insert_to_mongo(df: pd.DataFrame):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Convert DataFrame to dictionary records
    records = df.to_dict(orient='records')
    collection.insert_many(records)
    print(f"Inserted {len(records)} records into MongoDB.")
    client.close()


if __name__ == "__main__":
    from arxiv_loader import fetch_arxiv_data
    from html_loader import add_html_content

    df = fetch_arxiv_data("artificial intelligence", max_results=5)
    df = add_html_content(df)
    insert_to_mongo(df)
