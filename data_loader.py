# data_loader.py
import pandas as pd


def load_articles(csv_file: str) -> pd.DataFrame:
    """
    Load CSV into a pandas DataFrame.
    All columns are treated as strings for consistency.
    """
    df = pd.read_csv(csv_file, dtype=str)
    print(f"Loaded {len(df)} rows from {csv_file}")
    return df


if __name__ == "__main__":
    df = load_articles("articles.csv")  # replace with your CSV filename
    print(df)
