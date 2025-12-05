from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams
from pydantic import BaseModel
import numpy as np

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

collection_name = "test_collection"

# Create collection if it doesn't exist
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors=VectorParams(size=4, distance="Cosine")
    )

# Metadata model


class Chunk(BaseModel):
    text: str
    text_preview: str


chunk = Chunk(text="This is a test chunk",
              text_preview="Test chunk").model_dump()
vector = np.random.rand(4).tolist()

# Upsert point
client.upsert(
    collection_name=collection_name,
    points=[PointStruct(id=1, vector=vector, payload=chunk)]
)

# Search points
response = client.retrieve(
    collection_name=collection_name,
    ids=[1]
)

print("Retrieved points:", response)
