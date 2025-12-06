# html_loader.py
import pandas as pd
import requests
from bs4 import BeautifulSoup


def download_html(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""


def add_html_content(df: pd.DataFrame) -> pd.DataFrame:
    df['html_content'] = df['url'].apply(download_html)
    return df


if __name__ == "__main__":
    from arxiv_loader import fetch_arxiv_data
    df = fetch_arxiv_data("machine learning", max_results=5)
    df = add_html_content(df)
    print(df[['title', 'html_content']])
