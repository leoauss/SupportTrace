from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

class SemanticCache:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.similarity_threshold = 0.92
        self.cache = []
    
    def store(self, customer_text: str, reply: str, intent: str):
        embedding = self.model.encode(customer_text, convert_to_tensor=True)
        self.cache.append({"text": customer_text, "reply": reply, "intent": intent, "embedding": embedding})
    
    def lookup(self, customer_text: str):
        if len(self.cache) == 0:
            return None
        query_embedding = self.model.encode(customer_text, convert_to_tensor=True)
        best_score = 0.0
        best_reply = None
        best_intent = None

        for entry in self.cache:
            score = cos_sim(query_embedding, entry["embedding"]).item()

            if score > best_score:
                best_score = score
                best_reply = entry["reply"]
                best_intent = entry["intent"]
        
        if best_score > self.similarity_threshold:
            return best_reply, best_intent
        return None