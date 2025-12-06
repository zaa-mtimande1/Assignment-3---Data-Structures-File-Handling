# main_arxiv.py
import pandas as pd
from arxiv_loader import fetch_arxiv, fetch_html_content

# Fetch 10 articles for the query
df_arxiv = fetch_arxiv("quantum computing", max_results=10)

# Add HTML content column
df_arxiv = df_arxiv.apply(fetch_html_content, axis=1)

# Save for verification
df_arxiv.to_csv("arxiv_articles_with_html.csv", index=False)
print(df_arxiv)
