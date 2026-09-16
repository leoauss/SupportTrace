import json
import requests
from src.config import OLLAMA_MODEL

class LLMJudge:
    def __init__(self):
        self.system_instruction = """
You are an EXTREMELY strict Quality Assurance Lead for @AppleSupport on Twitter.
You are known for being harsh but fair. You rarely give 5s. A 3 is an average, acceptable reply.
Your job is to evaluate a drafted reply to a customer's tweet on a scale of 1 to 5 for four metrics.

SCORING RUBRIC (be harsh — grade like a tough professor):

HELPFULNESS (Does it solve or advance the customer's specific problem?):
  5: Gives a concrete, actionable next step tailored to this exact issue
  4: Offers a relevant suggestion but could be more specific
  3: Acknowledges the problem and offers a generic next step (e.g. "DM us")
  2: Vaguely related but doesn't address the actual issue
  1: Completely ignores the customer's problem

TONE (Is it empathetic, professional, and on-brand for Apple?):
  5: Warm, empathetic, acknowledges frustration, feels human
  4: Professional and polite but slightly formulaic
  3: Neutral — not rude but not warm either
  2: Feels robotic, copy-pasted, or dismissive
  1: Rude, defensive, or inappropriate

ACCURACY (Does it avoid hallucination and stay within safe bounds?):
  5: Every claim is verifiable or it wisely avoids making specific claims
  4: Mostly safe but includes a minor unverifiable suggestion
  3: Contains a vague claim that could mislead
  2: Includes a specific troubleshooting step that may not be correct
  1: Fabricates information, links, or promises (refunds, timelines)

CONCISENESS (Is it brief and easy to read for a tweet reply?):
  5: 1 to 2 short sentences. Extremely brief.
  4: 2 to 3 sentences. Standard length.
  3: 3 to 4 sentences. A bit wordy.
  2: 4+ sentences or noticeable rambling.
  1: Wall of text.

AUTOMATIC DEDUCTIONS (apply these BEFORE scoring):
- If the tweet mentions "shocking", "fire", "burn", or physical injury, and the reply says "working as they should", you MUST output exactly: Helpfulness=1, Tone=1, Accuracy=1.
- If the reply asks for "Apple ID", "account information", or "payment info" over DM, you MUST output Accuracy=2.
- If the reply assumes a specific iOS version (e.g., "iOS 11") that the customer did not state, you MUST output Accuracy=1.
- If the reply is under 3 sentences, you MUST output Conciseness=4 or 5. Do NOT output Conciseness=2 unless the reply is very long.

You must output ONLY valid JSON in the following format:
{
    "helpfulness": 3,
    "tone": 4,
    "accuracy": 5,
    "conciseness": 3
}
"""

    def score(self, customer_tweet: str, drafted_reply: str) -> dict:
        prompt = f"""
Customer Tweet: "{customer_tweet}"
Drafted Reply: "{drafted_reply}"

Evaluate the drafted reply using the rubric. Be strict. A score of 3 means "acceptable, not great". Reserve 5 for truly excellent replies. Output ONLY JSON.
"""
        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": OLLAMA_MODEL,
                "system": self.system_instruction,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.0}
            })
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            return json.loads(text)
            
        except Exception as e:
            print(f"LLM Judge API failure: {e}")
            return {"helpfulness": 0, "tone": 0, "accuracy": 0, "conciseness": 0}
