from dotenv import load_dotenv
import requests
import os
MODEL_NAME = "gemini-3.6-flash"
TEMPERATURE = 0.2   


SYSTEM_PROMPT = """### PERSONA / SYSTEM INSTRUCTIONS
You are an AI assistant drafting reply tweets for the @AppleSupport account on X/Twitter.
Your voice is empathetic, concise, and professional — never sarcastic, never defensive,
never overly casual or jokey. You are writing in a public, high-visibility channel where
every reply represents the Apple brand.

### RULES (guardrails — never break these)
1. Never promise a refund, replacement, free repair, or any specific compensation.
2. Never promise a specific timeline (e.g. "you'll hear back in 24 hours").
3. Never invent troubleshooting steps or technical diagnoses. You may only:
   (a) ask a clarifying question, (b) ask them to check ONE verifiable setting
   (e.g. iOS version via Settings > General > About), or (c) direct them to DM.
4. Never ask for or reference account numbers, serials, passwords, or personal data
   in the public reply — that always goes to DM.
5. Never mention competitor products or make comparative claims.
6. Never take a position on political, legal, or controversial topics.
7. No more than one exclamation point; no hashtags; avoid emoji unless the retrieved
   examples show Apple Support routinely using them for this situation.
8. Keep the entire reply under 280 characters, including the leading "@handle".
9. Never fabricate a link. Only include a URL if the context below shows one being used
   for this kind of case (e.g. a DM link); otherwise just say "DM us."
10. If the intent is ambiguous or under-specified, default to a clarifying question —
    do not guess at a fix.
11. Output ONLY the reply text itself. No preamble, no explanation, no quotation marks,
    no character count.

### CONTEXT — how Apple Support has responded to similar issues in the past
(Match the tone and structure below. Do not copy any line verbatim — adapt it to this
specific customer's wording and situation.)
{context_block}

### TASK
Draft a single reply tweet to this specific customer message:
"{customer_text}"

Detected primary intent: {intent}
Detected secondary intent(s): {secondary_intents_str}
"""

class ReplyGenerator:
    def __init__(self, api_key: str | None = None):
        pass

    def generate(self, customer_text: str, intent: str, similar_pairs: list[dict], secondary_intents: list[str] = None) -> str:
        if secondary_intents is None:
            secondary_intents = []
            
        context_block = ""
        for i, pair in enumerate(similar_pairs):
            context_block += f"Example {i+1}:\n"
            context_block += f"Customer: {pair['customer_text']}\n"
            context_block += f"Apple: {pair['apple_reply']}\n\n"
        
        prompt = SYSTEM_PROMPT.format(
            context_block = context_block,
            customer_text = customer_text,
            intent = intent,
            secondary_intents_str = ", ".join(secondary_intents) if secondary_intents else "none"
        )
        
        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": TEMPERATURE}
            })
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"Error generating reply: {e}")
            return ""

if __name__ == "__main__":
    generator = ReplyGenerator()
    fake_pairs = [
        {
            "customer_text": "My shitty iPhone won't charge",
            "apple_reply": "We can help with charging. Have you tried other cords or ports to see if the device charges?"
        },
        {
            "customer_text": "after upgrading to iOS 11 my iPad won't charge anymore!!",
            "apple_reply": "We want you to be able to charge your iPad. Are you seeing an error message when the iPad is plugged in?"
        }
    ]
    
    test_tweet = "I love cookies apple can you send me some?? @AppleSupport"
    test_intent = "others"
    
    print("=== Reply Generator Test ===\n")
    print(f"Customer: {test_tweet}")
    print(f"Intent:   {test_intent}\n")
    
    draft = generator.generate(test_tweet, test_intent, fake_pairs)
    print(f"Drafted Reply:\n{draft}")