# src/intent/classifier.py

import json
import os
import random
import time
import requests
from dataclasses import dataclass, field

from src.intent.taxonomy import (
    VALID_INTENTS,
    build_intent_description_block,
    build_few_shot_block,
)

TEMPERATURE = 0.0         

@dataclass
class IntentResult:
    """Output of the classifier for a single tweet."""
    primary_intent: str
    secondary_intents: list[str] = field(default_factory=list)
    confidence: float = 0.0
    risk_level: str = "low"
    raw_response: str = ""        
    error: str | None = None        

    @property
    def is_valid(self) -> bool:
        """Check that all returned intents are in the taxonomy."""
        if self.primary_intent not in VALID_INTENTS:
            return False
        return all(s in VALID_INTENTS for s in self.secondary_intents)


def _fallback_result(reason: str, raw: str = "", confidence: float = 0.0) -> IntentResult:
    """Single place that builds the 'give up' result, so classify() always
    returns something well-formed no matter which branch it exits from."""
    return IntentResult(
        primary_intent="other",
        secondary_intents=[],
        confidence=confidence,
        risk_level="low",
        raw_response=raw,
        error=reason,
    )



SYSTEM_PROMPT = """\
You are an intent classifier for @AppleSupport on Twitter.

Given a customer message, classify it using EXACTLY the intents listed below.
Do NOT invent new intent names.

INTENTS:
{intent_descriptions}

RULES:
- primary_intent: exactly ONE intent — the main reason the customer is writing.
- secondary_intents: zero or more DISTINCT intents also clearly present. Only add a
  secondary intent if removing it would cause a reader to misunderstand the ticket.
  Use an empty list if there's no secondary intent.
- confidence: a float between 0.0 and 1.0 indicating how confident you are in the
  primary intent classification. Use lower values (< 0.6) when the message is
  ambiguous, off-topic, or could reasonably fit multiple primary intents.
- risk_level: "low", "medium", or "high". 
  * high = physical harm, safety hazard, legal threat, medical emergency, property damage
  * medium = strong frustration, profanity, mentions of money loss
  * low = standard support request

DISAMBIGUATION (use these to resolve tricky cases):
- "how_to" vs OTHER CATEGORIES: Use "how_to" ONLY for general Apple ecosystem instructions. If the customer asks "how to" do something related to a specific category, use that specific category instead! For example:
  * "How do I switch my family subscription?" -> billing_subscription
  * "Can you explain the difference between iCloud plans?" -> icloud_storage
  * "When is the next watchOS update?" -> software_update
  * "How to transfer photos?" -> data_transfer
  * "Is the MacBook back in stock?" -> purchase_delivery
- "other" vs "how_to": If they ask a general question ("what's the capital of France", "can I talk to a human", "does Apple do trade-in events"), use "other", NOT "how_to".
- "device_issue" vs "performance": Use "device_issue" for PHYSICAL/HARDWARE problems. Use "performance" for SPEED/RESPONSIVENESS complaints where hardware is not damaged.
- "app_crash" vs "software_issue": Use "app_crash" when a specific app crashes/freezes. Use "software_issue" for system-wide bugs or glitches.
- "software_issue" vs "software_update": Use "software_update" only when stuck on or asking about an update process. If it broke "after an update", it's "software_issue".
- "content_dispute" vs "billing_subscription": Use "content_dispute" for unauthorized/unrecognized charges. Use "billing_subscription" for standard billing/pricing questions.

RESPOND WITH ONLY a valid JSON object, no markdown, no explanation:
{{"primary_intent": "...", "secondary_intents": [...], "confidence": 0.0, "risk_level": "low"}}
"""

FEW_SHOT_HEADER = """\

EXAMPLES:
{examples}

Now classify this customer message:
Customer: "{customer_text}"
"""

class IntentClassifier:
    """Few-shot intent classifier powered by Gemini."""

    def __init__(self, api_key: str | None = None):
        pass

        self._system_block = SYSTEM_PROMPT.format(
            intent_descriptions=build_intent_description_block()
        )
        self._examples_block = build_few_shot_block()

    def _build_prompt(self, text: str) -> str:
        """Combine system prompt + few-shot examples + the input tweet."""
        user_block = FEW_SHOT_HEADER.format(
            examples=self._examples_block,
            customer_text=text,
        )
        return self._system_block + user_block

    def _parse_response(self, raw: str) -> IntentResult:
        """Parse the JSON response from Gemini. Handles common formatting issues."""
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            cleaned = "\n".join(lines).strip()

        data = json.loads(cleaned) 

        result = IntentResult(
            primary_intent=data.get("primary_intent", "other"),
            secondary_intents=data.get("secondary_intents", []),
            confidence=float(data.get("confidence", 0.0)),
            risk_level=data.get("risk_level", "low"),
            raw_response=raw,
        )

        if result.primary_intent not in VALID_INTENTS:
            print(f"  WARNING: invalid primary_intent '{result.primary_intent}' → defaulting to 'other'")
            result.primary_intent = "other"
            result.confidence = max(result.confidence * 0.5, 0.1)

        result.secondary_intents = [
            s for s in result.secondary_intents if s in VALID_INTENTS
        ]

        return result

    def classify(self, text: str) -> IntentResult:
        """Classify a single customer tweet using local Llama 3.1."""
        prompt = self._build_prompt(text)

        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": TEMPERATURE}
            })
            response.raise_for_status()
            last_raw = response.json().get("response", "").strip()
        except Exception as e:
            return _fallback_result(f"api_error: {e}", raw="")

        try:
            return self._parse_response(last_raw)
        except json.JSONDecodeError as e:
            return _fallback_result(f"json_error: {e}", raw=last_raw, confidence=0.1)

    def classify_batch(self, texts: list[str], delay: float = 12.5) -> list[IntentResult]:
        """Classify a list of tweets with a delay between calls (rate limiting)."""
        results = []
        for i, text in enumerate(texts):
            if i > 0 and delay > 0:
                time.sleep(delay)
            result = self.classify(text)
            results.append(result)
            if result.error:
                print(f"  [{i+1}] fell back to 'other' — {result.error}")
            if (i + 1) % 10 == 0:
                print(f"  Classified {i+1}/{len(texts)}...")
        return results

if __name__ == "__main__":
    classifier = IntentClassifier()

    test_tweets = [
        "My iPhone screen is cracked after dropping it, help @AppleSupport",
        "Why does my phone die so fast after the iOS 17 update?? @AppleSupport",
        "@AppleSupport I can't log into my Apple ID, it says account is locked",
        "@AppleSupport WTF is wrong with you guys",
        "How do I transfer my data to my new iPhone? @AppleSupport",
    ]

    print("\n=== Intent Classification Test ===\n")
    for i, tweet in enumerate(test_tweets):
        if i > 0:
            print("  [Waiting 12s for rate limit...]")
            time.sleep(12.5)

        result = classifier.classify(tweet)
        secondary = ", ".join(result.secondary_intents) or "none"
        print(f"Tweet:     {tweet[:80]}...")
        print(f"Primary:   {result.primary_intent} (confidence: {result.confidence:.2f})")
        print(f"Secondary: {secondary}")
        print(f"Risk Level:{result.risk_level}")
        print(f"Valid:     {result.is_valid}")
        if result.error:
            print(f"Error:     {result.error}")
        print()