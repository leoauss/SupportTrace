import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

url_pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
mention_pattern = r'@[a-zA-Z0-9_]{1,15}'
punctuation_pattern = r'[^\w\s]'

def clean_text(text: str) -> str:
    text = re.sub(url_pattern, '', text)
    text = re.sub(mention_pattern, '', text)
    text = text.lower()
    text = re.sub(punctuation_pattern, '', text)
    text = ' '.join(text.split())
    return text

class TFIDFRetriever:
    def __init__(self, data_path: str = "data/processed/apple_first_turns.jsonl"):
        self.pairs = []

        with open(data_path, encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                if len(entry.get('apple_reply', '')) > 30:
                    self.pairs.append(entry)

        print(f"Retriever: loaded {len(self.pairs):,} pairs")
        cleaned_docs = [clean_text(p['customer_text']) for p in self.pairs]
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            ngram_range=(1, 2),
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(cleaned_docs)
        print(f"Retriever: TF-IDF matrix shape = {self.tfidf_matrix.shape}")

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        cleaned_query = clean_text(query)
        query_vec = self.vectorizer.transform([cleaned_query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        top_indices = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'customer_text': self.pairs[idx]['customer_text'],
                'apple_reply': self.pairs[idx]['apple_reply'],
                'similarity_score': float(scores[idx]),
            })

        return results

if __name__ == "__main__":
    retriever = TFIDFRetriever()

    test_queries = [
        "My iPhone won't charge anymore",
        "How do I transfer data to my new iPhone?",
        "I can't log into my Apple ID",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        results = retriever.retrieve(query, top_k=3)
        for i, r in enumerate(results):
            print(f"\n  [{i+1}] Score: {r['similarity_score']:.3f}")
            print(f"      Customer: {r['customer_text'][:100]}")
            print(f"      Apple:    {r['apple_reply'][:100]}")