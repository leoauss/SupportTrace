import pandas as pd

def filter_apple_conversations(
    df: pd.DataFrame, brand_id: str = "AppleSupport"
) -> pd.DataFrame:
    """Keep only tweets from threads that involve AppleSupport."""
    apple_rows = df[df['author_id'] == brand_id]

    apple_tweet_ids = set(apple_rows['tweet_id'])

    apple_reply_targets = set(apple_rows['in_response_to_tweet_id'].dropna())

    apple_df = df[
        (df['author_id'] == brand_id) |
        (df['in_response_to_tweet_id'].isin(apple_tweet_ids)) |
        (df['tweet_id'].isin(apple_reply_targets))
    ]

    print(f"Apple conversations: {len(apple_df):,} tweets")
    return apple_df