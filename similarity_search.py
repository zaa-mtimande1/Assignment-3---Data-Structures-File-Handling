import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load chunk embeddings
df = pd.read_csv("chunk_embeddings.csv")

# Convert list strings back to numpy arrays
df['embedding'] = df['embedding'].apply(lambda x: np.array(eval(x)))

# Compute cosine similarity with the first chunk
query_embedding = df['embedding'][0].reshape(1, -1)
similarities = cosine_similarity(
    query_embedding, np.stack(df['embedding'].values))[0]

# Show top similar chunks
top_indices = np.argsort(similarities)[::-1]
print("Top similar chunks:")
for idx in top_indices:
    print(
        f"Text: {df['text_chunk'][idx]}, Similarity: {similarities[idx]:.3f}")
