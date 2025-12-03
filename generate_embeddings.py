# generate_mock_embeddings.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Example article chunks
chunks = [
    "Machine learning is a subset of AI that uses data to learn.",
    "Deep learning involves neural networks with many layers.",
    "Data science combines domain expertise, programming, and statistics.",
    "Neural networks are inspired by the human brain."
]

# Generate proper mock embeddings (small vectors)
embeddings = [np.random.rand(5).tolist()
              for _ in chunks]  # convert arrays to lists

# Save to CSV
df = pd.DataFrame({"text_chunk": chunks, "embedding": embeddings})
df.to_csv("chunk_embeddings.csv", index=False)

# Test cosine similarity
sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
print("Sample similarity between first two chunks:", round(sim, 3))
