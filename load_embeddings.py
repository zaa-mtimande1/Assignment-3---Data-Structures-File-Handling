import pickle

# Load the embeddings file
with open("embeddings.pkl", "rb") as f:
    data = pickle.load(f)

# Check the type
print(type(data))          # Should show <class 'pandas.core.frame.DataFrame'>
print(data.columns)        # Should show Index(['title', 'chunk_embeddings'])

# Inspect the first row
print(data.iloc[0])

# Inspect the embedding of the first row
print(data.iloc[0]["chunk_embeddings"])
