# Run this ONCE to understand the data. Read every output carefully.

import pandas as pd
import json
from collections import Counter

df = pd.read_csv("data/raw/twcs.csv", dtype=str)
df['inbound'] = df['inbound'].map({'True': True, 'False': False})

print("=" * 60)
print("1. BASIC SHAPE")
print("=" * 60)
print(f"Rows: {len(df):,}")
print(f"Columns: {list(df.columns)}")
print(f"Inbound (customer) tweets:  {df['inbound'].sum():,}")
print(f"Outbound (brand) tweets:    {(~df['inbound']).sum():,}")


print("\n" + "=" * 60)
print("2. TOP 20 BRANDS BY OUTBOUND TWEET VOLUME")
print("=" * 60)
outbound = df[df['inbound'] == False]
top_brands = outbound['author_id'].value_counts().head(20)
print(top_brands)


apple_id = outbound['author_id'].value_counts().index[0]
print(f"\n→ Top brand (assumed AppleSupport): {apple_id}")
df['text_len'] = df['text'].fillna('').str.len()

print("\n" + "=" * 60)
print("3. APPLE-SPECIFIC STATS")
print("=" * 60)
apple_df = df[df['author_id'] == apple_id]
customer_df = df[df['inbound'] == True]

print(f"Apple outbound tweets: {len(apple_df):,}")


apple_replied_to = set(apple_df['in_response_to_tweet_id'].dropna())
print(f"Unique customer tweets Apple replied to: {len(apple_replied_to):,}")


print("\n" + "=" * 60)
print("4. TWEET LENGTH DISTRIBUTION")
print("=" * 60)

print("Customer tweet lengths:")
print(df[df['inbound'] == True]['text_len'].describe())
print("\nApple reply lengths:")
print(apple_df['text_len'].describe())

print("\n" + "=" * 60)
print("5. NULL / MISSING VALUES")
print("=" * 60)
print(df[['tweet_id', 'author_id', 'inbound', 'text',
          'in_response_to_tweet_id', 'response_tweet_id']].isnull().sum())

print("\n" + "=" * 60)
print("6. SAMPLE APPLE REPLY PATTERNS")
print("=" * 60)

print("\n--- 10 random Apple replies ---")
for text in apple_df['text'].sample(10, random_state=42):
    print(f"  • {text[:120]}")


dm_replies = apple_df['text'].str.contains('DM|direct message', case=False, na=False)
print(f"\nApple replies containing 'DM': {dm_replies.sum():,} ({dm_replies.mean()*100:.1f}%)")


print("\n" + "=" * 60)
print("7. SAMPLE CUSTOMER MESSAGES (READ THESE FOR INTENT IDEAS)")
print("=" * 60)

replied_customers = df[
    (df['inbound'] == True) & 
    (df['tweet_id'].isin(apple_replied_to))
]
print(f"Customer messages that got a reply: {len(replied_customers):,}")
print("\n--- 20 random customer messages ---")
for text in replied_customers['text'].sample(20, random_state=42):
    print(f"  • {text[:120]}")


print("\n" + "=" * 60)
print("8. PII MASK FREQUENCY")
print("=" * 60)

for mask in ['__email__', '__phone__', '__url__']:
    count = df['text'].str.contains(mask, na=False).sum()
    print(f"Tweets with {mask}: {count:,}")


print("\n" + "=" * 60)
print("9. TEMPORAL DISTRIBUTION")
print("=" * 60)
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
apple_df_dated = apple_df.copy()
apple_df_dated['created_at'] = pd.to_datetime(apple_df_dated['created_at'], errors='coerce')
print("Date range of dataset:")
print(f"  From: {df['created_at'].min()}")
print(f"  To:   {df['created_at'].max()}")


print("\n" + "=" * 60)
print("10. SAMPLE FULL THREAD (read this to understand the structure)")
print("=" * 60)

tweet_lookup = df.set_index('tweet_id').to_dict('index')


for cust_tweet_id in replied_customers['tweet_id'].sample(50, random_state=1):
    apple_replies = apple_df[
        apple_df['in_response_to_tweet_id'] == cust_tweet_id
    ]
    if len(apple_replies) > 0:
        print(f"\n Customer [{cust_tweet_id}]:")
        print(f"   {tweet_lookup[cust_tweet_id]['text']}")
        for _, reply in apple_replies.iterrows():
            print(f"\n Apple [{reply['tweet_id']}]:")
            print(f"   {reply['text']}")
        break
