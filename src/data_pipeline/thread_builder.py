import networkx as nx
import pandas as pd
import json
from pathlib import Path


def build_conversation_graph(df: pd.DataFrame) -> tuple[nx.DiGraph, pd.Series]:
    known_ids = set(df['tweet_id'])

    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_node(row['tweet_id'], **row.to_dict())

    has_parent = df['in_response_to_tweet_id'].notna()
    parent_exists = df['in_response_to_tweet_id'].isin(known_ids)

    resolved = df[has_parent & parent_exists]
    dangling = df[has_parent & ~parent_exists]
    roots = df[~has_parent]

    G.add_edges_from(
        resolved[['in_response_to_tweet_id', 'tweet_id']].itertuples(index=False, name=None)
    )

    status = pd.Series('reply_resolved', index=df.index)
    status[roots.index] = 'root'
    status[dangling.index] = 'reply_dangling'

    print(f"{len(roots):,} roots, {len(resolved):,} resolved replies, "
          f"{len(dangling):,} dangling references (parent not in dataset)")

    return G, status


def extract_first_turns(G: nx.DiGraph) -> list:
    roots = [n for n in G.nodes if G.in_degree(n) == 0]
    pairs = []

    for root_id in roots:
        first = G.nodes[root_id]
        if first.get('inbound') is not True:
            continue

        for child_id in G.successors(root_id):
            second = G.nodes[child_id]
            if second.get('inbound') is False:
                subtree_len = len(list(nx.dfs_preorder_nodes(G, child_id))) + 1
                pairs.append({
                    'customer_text': first['text'],
                    'apple_reply': second['text'],
                    'thread_length': subtree_len,
                })

    print(f"Extracted {len(pairs):,} first-turn pairs")
    return pairs


def save_first_turns(pairs: list, path: str = "data/processed/apple_first_turns.jsonl"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for p in pairs:
            f.write(json.dumps(p, ensure_ascii=False) + '\n')
    print(f"Saved {len(pairs):,} pairs to {path}")