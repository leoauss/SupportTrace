import pandas as pd
from pathlib import Path

def load_raw(path: str = "data/raw/twcs.csv") -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No file at {path}")

    df = pd.read_csv(path, dtype=str)

    df['inbound'] = df['inbound'].str.strip() == 'True'
    df['created_at'] = pd.to_datetime(
        df['created_at'], format='%a %b %d %H:%M:%S %z %Y', errors='coerce'
    )

    n_bad_dates = df['created_at'].isna().sum()
    if n_bad_dates:
        pct = n_bad_dates / len(df) * 100
        print(f"Warning: {n_bad_dates:,} rows ({pct:.2f}%) failed created_at parsing → NaT")

    df['text'] = df['text'].fillna('').str.strip()
    df = df[df['text'] != ''].reset_index(drop=True)

    df['response_tweet_id'] = df['response_tweet_id'].apply(
        lambda x: [i.strip() for i in str(x).split(',')] if pd.notna(x) else []
    )

    print(f"Loaded {len(df):,} tweets")
    return df