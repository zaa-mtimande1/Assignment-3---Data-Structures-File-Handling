# arxiv_loader.py
import pandas as pd
import requests
import xml.etree.ElementTree as ET


def fetch_arxiv_data(query: str, max_results: int = 10) -> pd.DataFrame:
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}"
    response = requests.get(url)
    response.raise_for_status()
    root = ET.fromstring(response.content)

    entries = []
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text
        authors = ', '.join([author.find(
            'atom:name', ns).text for author in entry.findall('atom:author', ns)])
        abstract = entry.find('atom:summary', ns).text
        arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
        published = entry.find('atom:published', ns).text

        entries.append({
            'title': title,
            'author': authors,
            'abstract': abstract,
            'year': published[:4],
            'journal': '',  # Can leave blank
            'url': f"https://arxiv.org/abs/{arxiv_id}",
            'pdf_link': f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            'arxiv_id': arxiv_id
        })

    df = pd.DataFrame(entries, dtype=str)
    return df


if __name__ == "__main__":
    df = fetch_arxiv_data("quantum computing", max_results=5)
    print(df)
