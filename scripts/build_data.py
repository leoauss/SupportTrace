import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_pipeline.ingest import load_raw
from src.data_pipeline.filter_brand import filter_apple_conversations
from src.data_pipeline.thread_builder import build_conversation_graph, extract_first_turns, save_first_turns

df = load_raw()

apple_df = filter_apple_conversations(df)

G, status = build_conversation_graph(apple_df)

pairs = extract_first_turns(G)

save_first_turns(pairs)

print(f"\n--- Sample pair ---")
if pairs:
    print(f"Customer: {pairs[0]['customer_text']}")
    print(f"Apple:    {pairs[0]['apple_reply']}")
else:
    print("No pairs extracted — check the pipeline before going further.")