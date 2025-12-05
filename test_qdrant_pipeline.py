# test_qdrant_pipeline.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, Filter, FieldCondition, MatchValue
from pydantic import BaseModel
import uuid

# -------------------------------
# 1️⃣ Define a Pydantic model for chunk metadata
# -------------------------------


class ChunkMetadata(BaseModel):
    article_id: str
    chunk_index: int
    text_preview: str  # optional short preview


# -------------------------------
# 2️⃣ Connect to Qdrant
# -------------------------------
client = QdrantClient(url="http://localhost:6333")

collection_name = "articles_chunks"

# Create collection if it doesn't exist
if collection_name not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )
    print(f"Collection '{collection_name}' created!")
else:
    print(f"Collection '{collection_name}' already exists.")

# -------------------------------
# 3️⃣ Prepare a test chunk
# -------------------------------
article_id = "test_article_1"
chunk_index = 0
chunk_text = "This is a test chunk of text for Qdrant semantic search."
chunk_id = str(uuid.uuid4())  # unique ID for the chunk

metadata = ChunkMetadata(
    article_id=article_id,
    chunk_index=chunk_index,
    text_preview=chunk_text[:50]
).dict()

# Dummy embedding (replace with your real embedding function)
vector = [0.1] * 1536

# -------------------------------
# 4️⃣ Insert the test chunk into Qdrant
# -------------------------------
client.upsert(
    collection_name=collection_name,
    points=[
        {
            "id": chunk_id,
            "vector": vector,
            "payload": metadata
        }
    ]
)
print("Test chunk inserted!")

# -------------------------------
# 5️⃣ Perform a semantic search
# -------------------------------
query_text = "test Qdrant search"
query_vector = [0.1] * 1536  # same dummy vector

results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=3
)

print("\nSearch results:")
for hit in results:
    print(f"ID: {hit.id}, Score: {hit.score}, Payload: {hit.payload}")
