# semantic_pipeline.py
import os
import pandas as pd
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import google.generativeai as genai

# -------------------------------
# Load Gemini API Key
# -------------------------------
load_dotenv()
GENAI_API_KEY = os.getenv("AIzaSyB-2cDJwA--3rnZfpAmGI1PwDJVh9Kx57g")
genai.api_key = GENAI_API_KEY

# -------------------------------
# Qdrant setup
# -------------------------------
COLLECTION_NAME = "my_collection"

client = QdrantClient(path="./qdrant_local")

# Delete collection if exists
try:
    client.delete_collection(COLLECTION_NAME)
except Exception:
    pass

# Create collection with correct vector size (match Gemini embeddings)
VECTOR_SIZE = 384  # Gemini embedding size
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=VECTOR_SIZE,
        distance=Distance.COSINE
    )
)
print(
    f"Collection '{COLLECTION_NAME}' created with vector size {VECTOR_SIZE}.")

# -------------------------------
# Example DataFrame (replace with your articles)
# -------------------------------
data = {
    "point_id": [1, 2],
    "text": [
        "This is the first chunk of text.",
        "Here is the second chunk of text."
    ]
}
df = pd.DataFrame(data)

# -------------------------------
# Functions
# -------------------------------


def embed(text: str):
    """Get Gemini embedding for text."""
    response = genai.embed_content(model="embed-text-v1", content=text)
    return response.embedding


def chunk_exists(point_id):
    """Check if a point already exists in Qdrant."""
    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=100
    )
    if points is None:
        return False
    for point in points:
        if point.id == point_id:
            return True
    return False


# -------------------------------
# Process DataFrame
# -------------------------------
for _, row in df.iterrows():
    if chunk_exists(row["point_id"]):
        print(f"Chunk {row['point_id']} already exists.")
        continue

    # Generate embedding
    vector = embed(row["text"])

    # Upsert into Qdrant
    point = PointStruct(
        id=row["point_id"],
        vector=vector,
        payload={"text": row["text"]}
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])
    print(f"Inserted chunk {row['point_id']}.")

# -------------------------------
# Semantic search function
# -------------------------------


def semantic_search(query: str, top_k: int = 3):
    query_vector = embed(query)
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    for result in search_results:
        print(
            f"ID: {result.id}, Score: {result.score}, Text: {result.payload['text']}")


# -------------------------------
# Example search
# -------------------------------
print("\nSearch results for 'first chunk':")
semantic_search("first chunk")
