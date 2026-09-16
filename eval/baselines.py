from src.retrieval.retriever import TFIDFRetriever
from src.agent import AutoResponse, EscalationResponse

class TrivialBaseline:
    """
    The simplest baseline: always outputs intent='other' and a generic reply.
    Never escalates.
    """
    def process(self, customer_text: str):
        return AutoResponse(drafted_reply="Please DM us for more help.", intent="other")


class SimpleBaseline:
    """
    A step up: skips the LLM and intent classification.
    Uses TF-IDF to find the most similar historical tweet and returns its reply verbatim.
    Never escalates.
    """
    def __init__(self):
        self.retriever = TFIDFRetriever()
        
    def process(self, customer_text: str):
        similar_pairs = self.retriever.retrieve(customer_text)
        
        if similar_pairs:
            best_reply = similar_pairs[0]["apple_reply"]
            return AutoResponse(drafted_reply=best_reply, intent="other")
        else:
            return AutoResponse(drafted_reply="Please DM us so we can look into this.", intent="other")
