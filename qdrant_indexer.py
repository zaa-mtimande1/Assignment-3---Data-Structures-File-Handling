# qdrant_indexer.py
from typing import List, Dict, Optional, Any, Iterable, Tuple
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest_models
import pandas as pd
import hashlib
from tqdm.auto import tqdm
import math

# ---------- Configuration ----------
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_COLLECTION = "articles_chunks"
VECTOR_SIZE = 1536   # change to the dimensionality of your embedding model
DISTANCE = rest_models.Distance.COSINE  # or DOT, EUCLID

# ---------- Helpers ----------


def deterministic_id_from_text(text: str) -> str:
    """Deterministic id for a chunk (so the same text -> same id)."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# ---------- Pydantic model for metadata ----------
class ChunkMetadata(BaseModel):
    article_id: str
    chunk_index: int
    chunk_text_excerpt: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    # add other fields that are helpful to retrieve later


# ---------- Qdrant client and collection utilities ----------
def create_qdrant_client(host: str = QDRANT_HOST, port: int = QDRANT_PORT, api_key: Optional[str] = None) -> QdrantClient:
    if api_key:
        return QdrantClient(url=f"http://{host}:{port}", api_key=api_key)
    return QdrantClient(url=f"http://{host}:{port}")


def ensure_collection(client: QdrantClient, collection_name: str = QDRANT_COLLECTION, vector_size: int = VECTOR_SIZE, distance: rest_models.Distance = DISTANCE):
    """
    Create collection if it doesn't exist. Safe to call repeatedly.
    """
    from qdrant_client.http import models as m
    try:
        client.get_collection(collection_name)
        # collection exists
    except Exception:
        # Create with default payload schema (we don't need a strict schema here)
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=m.VectorParams(size=vector_size, distance=distance),
        )


# ---------- Save / check chunk functions ----------
def save_single_chunk(
    client: QdrantClient,
    collection_name: str,
    chunk_text: str,
    metadata: ChunkMetadata,
    vector: List[float]
) -> None:
    """
    Save a single chunk as a point into Qdrant.
    Uses deterministic ID from chunk_text to avoid duplicates.
    """
    point_id = deterministic_id_from_text(chunk_text)
    point = rest_models.PointStruct(
        id=point_id,
        vector=vector,
        payload=metadata.dict()
    )
    client.upsert(collection_name=collection_name, points=[point])


def check_existing_point_ids(client: QdrantClient, collection_name: str, ids: Iterable[str]) -> set:
    """
    Given a list/iterable of point ids (strings or ints), returns a set of ids that currently exist in Qdrant.
    Uses `retrieve` / `get_points` style API via client.retrieve to look up many ids at once (batched).
    """
    ids = list(ids)
    existing = set()
    batch_size = 256
    for i in range(0, len(ids), batch_size):
        batch = ids[i: i + batch_size]
        # `retrieve` is provided by qdrant-client: it returns found points
        resp = client.retrieve(collection_name=collection_name,
                               ids=batch, with_payload=False, with_vector=False)
        # resp is a list of PointStruct-like objects for found ids
        # some versions return empty list for missing ids; iterate safely:
        for p in resp:
            # p.id exists
            existing.add(str(p.id))
    return existing


# ---------- Chunking & DataFrame explosion ----------
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Simple character-based chunking. Returns list of chunk strings.
    You can replace with token-based chunking (tiktoken) if preferred.
    """
    if not text:
        return []
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap if end < L else end
    return chunks


def explode_articles_to_chunks(df: pd.DataFrame,
                               text_column: str = "text",
                               article_id_column: str = "article_id",
                               chunk_size: int = 1000,
                               overlap: int = 200) -> pd.DataFrame:
    """
    Input: DataFrame with at least columns [article_id_column, text_column].
    Output: DataFrame with one row per chunk:
      - article_id
      - chunk_index
      - chunk_text
      - chunk_id (deterministic from text)
    """
    rows = []
    for _, row in df.iterrows():
        article_id = str(row[article_id_column])
        text = row[text_column]
        chunks = chunk_text(text or "", chunk_size=chunk_size, overlap=overlap)
        for i, ch in enumerate(chunks):
            chunk_id = deterministic_id_from_text(ch)
            rows.append({
                "article_id": article_id,
                "chunk_index": i,
                "chunk_text": ch,
                "chunk_id": chunk_id
            })
    chunks_df = pd.DataFrame(rows)
    return chunks_df


# ---------- Embedding orchestration ----------
def compute_embeddings_for_texts(texts: List[str], embed_fn, batch_size: int = 64) -> List[List[float]]:
    """
    embed_fn: a function that accepts List[str] and returns List[List[float]]
    e.g. embed_fn = lambda texts: openai_embeddings_call(texts)
    This function batches into `batch_size` to avoid memory/external API limits.
    """
    all_vectors = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        vectors = embed_fn(batch)
        all_vectors.extend(vectors)
    return all_vectors


# ---------- End-to-end index update function ----------
def upsert_missing_chunks(
    client: QdrantClient,
    collection_name: str,
    chunks_df: pd.DataFrame,
    embed_fn,
    metadata_fields: Optional[List[str]] = None,
    batch_size_upsert: int = 128
) -> Tuple[int, int]:
    """
    - chunks_df must contain columns: ['chunk_id', 'chunk_text', 'article_id', 'chunk_index']
    - embed_fn is a function that takes List[str] -> List[List[float]]
    Returns (num_upserted, num_already_present)
    """
    # ensure collection exists
    ensure_collection(client, collection_name)

    # All chunk ids we want to ensure in DB:
    chunk_ids = chunks_df["chunk_id"].astype(str).tolist()
    existing_ids = check_existing_point_ids(client, collection_name, chunk_ids)
    to_add_df = chunks_df[~chunks_df["chunk_id"].astype(
        str).isin(existing_ids)].copy()

    num_already = len(chunks_df) - len(to_add_df)
    num_upserted = 0

    if to_add_df.empty:
        return (0, num_already)

    # compute embeddings only for missing chunks
    texts = to_add_df["chunk_text"].tolist()
    vectors = compute_embeddings_for_texts(texts, embed_fn)

    # prepare points and upsert in batches
    points = []
    for (idx, row), vector in zip(to_add_df.iterrows(), vectors):
        metadata = ChunkMetadata(
            article_id=str(row["article_id"]),
            chunk_index=int(row["chunk_index"]),
            chunk_text_excerpt=(row["chunk_text"][:300]
                                if row["chunk_text"] else None),
            # optionally include row.get('url') etc
        ).dict()
        p = rest_models.PointStruct(
            id=str(row["chunk_id"]),
            vector=vector,
            payload=metadata
        )
        points.append(p)

        # batch upsert
        if len(points) >= batch_size_upsert:
            client.upsert(collection_name=collection_name, points=points)
            num_upserted += len(points)
            points = []

    # upsert remainder
    if points:
        client.upsert(collection_name=collection_name, points=points)
        num_upserted += len(points)

    return (num_upserted, num_already)


# ---------- Search function ----------
def semantic_search(
    client: QdrantClient,
    collection_name: str,
    query: str,
    embed_query_fn,
    top_k: int = 5,
    with_payload: bool = True
) -> List[Dict[str, Any]]:
    """
    1) embed the query using embed_query_fn
    2) call client.search(...)
    3) returns list of result dicts with score, payload, id
    """
    q_vec = embed_query_fn([query])[0]
    hits = client.search(
        collection_name=collection_name,
        query_vector=q_vec,
        limit=top_k,
        with_payload=with_payload,
        with_vector=False
    )
    results = []
    for hit in hits:
        results.append({
            "id": str(hit.id),
            "score": hit.score,
            "payload": hit.payload
        })
    return results


# ---------- Example usage (replace embed_fn placeholders) ----------
if __name__ == "__main__":
    # Example placeholder embed functions:
    # Replace with your real embedding logic (OpenAI, sentence-transformers, etc.)
    def example_embed_fn(texts: List[str]) -> List[List[float]]:
        # Dummy embeddings for demonstration (DO NOT use in prod)
        import random
        return [[random.random() for _ in range(VECTOR_SIZE)] for _ in texts]

    client = create_qdrant_client()
    ensure_collection(client)

    # Example: load your articles DataFrame
    # df = pd.read_parquet("articles.parquet")  # must have columns article_id, text
    # For demo create a tiny DF:
    df = pd.DataFrame([
        {"article_id": "a1", "text": "This is the long article text A. " * 40},
        {"article_id": "a2", "text": "Another article B about something interesting. " * 30},
    ])

    chunks_df = explode_articles_to_chunks(df, text_column="text", article_id_column="article_id",
                                           chunk_size=800, overlap=128)
    print(f"Total chunks produced: {len(chunks_df)}")

    upserted, already = upsert_missing_chunks(
        client, QDRANT_COLLECTION, chunks_df, example_embed_fn)
    print(f"Upserted {upserted} points, {already} already present.")

    # Semantic search demo
    def example_query_embed_fn(texts):
        return example_embed_fn(texts)

    results = semantic_search(
        client, QDRANT_COLLECTION, "what is interesting about article A?", example_query_embed_fn)
    for r in results:
        print(r)
