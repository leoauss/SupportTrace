# SupportTrace 🍎🤖

An intelligent, multi-stage AI customer support agent pipeline built to process and respond to inbound customer queries on X/Twitter. Optimized and evaluated on the `@AppleSupport` dataset.

## 🌟 Headline Results
Our end-to-end pipeline achieves human-level triage and safety routing using completely local, open-source models:
* **Intent Classification Accuracy**: `~86%` (across 15+ complex categories)
* **Escalation Precision**: `~83%` (safety hazards, legal threats, abuse are correctly routed to humans)
* **LLM Judge Calibration**: Pearson Correlation `0.744` (Strong Agreement with human QA graders)

---

## 🏗️ Architecture
The pipeline is designed for safety, speed, and brand consistency. It consists of four main components:

1. **Intent Classifier (`src.intent.classifier`)**: Uses few-shot prompting to categorize the inbound tweet into a strict taxonomy (e.g., `device_issue`, `billing_subscription`, `how_to`).
2. **Escalation Decider (`src.escalation.decider`)**: Acts as a safety net. If a tweet contains physical injury, severe overheating, or legal threats, it instantly bypasses the AI and routes to a human agent.
3. **TF-IDF Retriever (`src.retrieval.retriever`)**: Searches a vector space of 80,000+ historical, authentic `@AppleSupport` replies. If a highly similar historical query is found (>90% similarity), the agent instantly returns the cached human reply, saving LLM compute and guaranteeing brand safety.
4. **Reply Generator (`src.generation.reply_generator`)**: If no historical match exists, the LLM drafts a custom, empathetic, and concise reply (under 280 characters) strictly adhering to Apple's brand voice.

---

## 📊 Dataset
The pipeline is built on the [Kaggle Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter) dataset.
* **Training/Retrieval Set**: 80,000+ real `@AppleSupport` interactions.
* **Golden Evaluation Set**: A stratified, hand-labeled set of 200 tweets containing authentic queries, synthetic edge cases (multi-intent, ultra-short), and adversarial safety tests (e.g., "my phone exploded").

---

## 🚀 Reproduction Guide
You can completely replicate our headline results locally in under 15 minutes.

### 1. Prerequisites
* **Python 3.10+**
* **Ollama**: You must have [Ollama](https://ollama.com/) installed and running locally.

Pull the required model (this takes a few minutes depending on your internet connection):
```bash
ollama pull llama3.1:8b
```

### 2. Setup the Repository
Clone the repository and install the dependencies:
```bash
git clone https://github.com/leoauss/SupportTrace.git
cd SupportTrace
pip install -r requirements.txt
```
*(Optional) Edit the `.env` file if you wish to swap the model from `llama3.1:8b` to something else.*

### 3. Reproduce the Benchmarks

**A. Pipeline Accuracy & Escalation Metrics**
Run the core evaluation against the 200-tweet Golden Set to verify the 86% accuracy and 83% escalation precision:
```bash
python -m eval.run_eval
```
*(Note: Since this runs 200 zero-shot inference passes, this may take 5-10 minutes depending on your GPU).*

**B. LLM Judge Calibration**
Verify that our automated LLM Judge grades replies exactly like a human QA lead (Pearson Correlation > 0.70):
```bash
python -m eval.judge_calibration
```

### 4. Run the Agent Interactively
Want to see the agent handle a severe safety hazard versus a standard support request? Run the interactive demo:
```bash
python -m src.agent
```

Or import it directly into your own Python scripts:
```python
from src.agent import SupportTrace

agent = SupportTrace()
response = agent.process("My iPhone screen is cracked and it's getting really hot, how do I fix it?")
print(response)
```
