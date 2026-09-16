from src.intent.classifier import IntentClassifier
from src.retrieval.retriever import TFIDFRetriever
from src.escalation.decider import EscalationDecider
from src.generation.reply_generator import ReplyGenerator
from src.caching.semantic_cache import SemanticCache

from dataclasses import dataclass

@dataclass
class AutoResponse:
    drafted_reply: str
    intent: str

@dataclass
class EscalationResponse:
    reason: str
    intent: str

class SupportTrace:
    def __init__(self):
        self.cacher = SemanticCache()
        self.classifier = IntentClassifier()
        self.retriever = TFIDFRetriever()
        self.decider = EscalationDecider()
        self.generator = ReplyGenerator()

    def process(self, customer_text: str):
        cache_result = self.cacher.lookup(customer_text)
        if cache_result is not None:
            cached_reply, cached_intent = cache_result
            return AutoResponse(cached_reply, cached_intent)
        
        intent_result = self.classifier.classify(customer_text)
        escalation_decision = self.decider.decide(customer_text, intent_result)
        if escalation_decision.should_escalate:
            return EscalationResponse(escalation_decision.reason, intent_result.primary_intent)
            
        similar_pairs = self.retriever.retrieve(customer_text)
        if not intent_result.secondary_intents and similar_pairs and similar_pairs[0]["similarity_score"] > 0.90:
            historical_reply = similar_pairs[0]["apple_reply"]
            self.cacher.store(customer_text, historical_reply, intent_result.primary_intent)
            return AutoResponse(historical_reply, intent_result.primary_intent)
        
        draft = self.generator.generate(customer_text, intent_result.primary_intent, similar_pairs, intent_result.secondary_intents)
        self.cacher.store(customer_text, draft, intent_result.primary_intent)
        return AutoResponse(draft, intent_result.primary_intent)

if __name__ == "__main__":
    print("Loading agent... (this may take a few seconds to build the TF-IDF matrix)")
    agent = SupportTrace()
    
    test_tweets = [
        "these trees and changes in Apple Maps caused me to total my car how do I turn that off! What a crappy night! Everyone is safe though.",
        "my Apple Watch Series 8 caused a burn on my wrist. This is shocking and unacceptable for a product from such a trusted brand. I need answers and a resolution immediately.",
        "Hey @AppleSupport my iPhone 15 (purchased May 24) charging cable has turned black This surely isn’t normal or safe",
        "Your cord almost burned my house down and your customer service rep said “I must’ve unplugged it wrong” is he f’n kidding me?"
    ]
    
    for tweet in test_tweets:
        print(f"\n{'-'*60}")
        print(f"Customer: {tweet}")
        response = agent.process(tweet)
        
        if isinstance(response, EscalationResponse):
            print(f"[!] ESCALATED [!]")
            print(f"Intent: {response.intent}")
            print(f"Reason: {response.reason}")
        else:
            print(f"[OK] AUTO-REPLY DRAFTED [OK]")
            print(f"Intent: {response.intent}")
            print(f"Draft:  {response.drafted_reply}")
