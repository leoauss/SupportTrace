import re
from dataclasses import dataclass
from src.intent.classifier import IntentResult

@dataclass
class EscalationDecision:
    should_escalate: bool
    reason: str

class EscalationDecider:
    def __init__(self):
        # Single-word triggers (checked after stripping punctuation)
        self.risk_keywords = [
            "sue", "sued", "suing", "lawyer", "attorney", "lawsuit",
            "death", "died", "kill", "killed",
            "scam", "scammed", "fraud", "fraudulent",
            "police", "fbi", "ftc",
            "burn", "burned", "burnt", "burning", "fire", "smoke", "smoking",
            "blast", "explode", "exploded", "explosion",
            "injury", "injured", "hospital", "emergency", "ambulance",
        ]
        
        # Multi-word phrases (checked via substring match on lowered text)
        self.risk_phrases = [
            "class action", "small claims", "consumer protection",
            "burned my", "caught fire", "almost died",
            "child safety", "kids safety",
            "going to sue", "i will sue", "hear from my lawyer",
        ]
        
        self.email_pattern = r'[\w\.-]+@[\w\.-]+'
        self.phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        
        # Intents that always require a human
        self.escalate_intents = []
    
    def decide(self, text: str, intent_result: IntentResult) -> EscalationDecision:
        text_lower = text.lower()
        
        # 1. Low confidence + not 'other' → escalate
        # We don't escalate 'other' because it catches trolls/spam/gibberish
        if intent_result.confidence < 0.4 and intent_result.primary_intent != "other":
            return EscalationDecision(True, f"Confidence is too low ({intent_result.confidence}) for a valid intent")
        
        # 2. Classifier flagged high risk
        if getattr(intent_result, 'risk_level', 'low') == "high":
            return EscalationDecision(True, "High risk level detected by classifier")
        
        # 3. Intent-based escalation
        if intent_result.primary_intent in self.escalate_intents:
            return EscalationDecision(True, f"Intent '{intent_result.primary_intent}' requires escalation")
        
        # 4. PII detection
        if re.search(self.email_pattern, text):
            return EscalationDecision(True, "Email address found in text")
        if re.search(self.phone_pattern, text):
            return EscalationDecision(True, "Phone number found in text")

        # 5. Single-word keyword scan
        for word in text_lower.split():
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word in self.risk_keywords:
                return EscalationDecision(True, f"High-risk keyword found: {clean_word}")
        
        # 6. Multi-word phrase scan
        for phrase in self.risk_phrases:
            if phrase in text_lower:
                return EscalationDecision(True, f"High-risk phrase found: '{phrase}'")

        return EscalationDecision(False, "No issues")