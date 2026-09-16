import csv
import json
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.agent import SupportTrace, AutoResponse, EscalationResponse
from eval.baselines import TrivialBaseline, SimpleBaseline
from eval.metrics import compute_intent_metrics, compute_escalation_metrics, compute_rouge
from eval.llm_judge import LLMJudge

def run_evaluation(csv_path: str, limit: int = None, use_judge: bool = False):
    agent = SupportTrace()
    trivial = TrivialBaseline()
    simple = SimpleBaseline()
    
    judge = LLMJudge() if use_judge else None
    
    true_intents = []
    true_escalations = []
    
    agent_intents = []
    agent_escalations = []
    agent_replies = []
    
    trivial_intents = []
    trivial_escalations = []
    
    simple_intents = []
    simple_escalations = []
    simple_replies = []
    
    retrieved_references = []
    
    judge_scores = []
    
    detail_rows = []
    
    print(f"Loading {csv_path}...")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    if limit:
        rows = rows[:limit]
        
    print(f"Starting evaluation on {len(rows)} tweets...")
    
    for i, row in enumerate(rows):
        tweet = row["Tweet Text"]
        true_intent = row["Primary Intent"].strip()
        true_escalation = str(row["pass to human"]).strip().upper() == "TRUE"
        
        true_intents.append(true_intent)
        true_escalations.append(true_escalation)
        
        print(f"[{i+1}/{len(rows)}] Processing: {tweet[:50]}...")
        
        t_res = trivial.process(tweet)
        trivial_intents.append(t_res.intent)
        trivial_escalations.append(False)
        
        s_res = simple.process(tweet)
        simple_intents.append(s_res.intent)
        simple_escalations.append(False) 
        simple_replies.append(s_res.drafted_reply)
        
        a_res = agent.process(tweet)
        
        agent_intents.append(a_res.intent)
        is_escalated = isinstance(a_res, EscalationResponse)
        agent_escalations.append(is_escalated)
        
        agent_reply_text = None
        if not is_escalated:
            agent_reply_text = a_res.drafted_reply
        
        agent_replies.append(agent_reply_text)
        
        retrieved_references.append(s_res.drafted_reply)
            
        j_scores = None
        if use_judge and agent_reply_text:
            j_scores = judge.score(tweet, agent_reply_text)
            judge_scores.append(j_scores)
        
        detail_rows.append({
            "tweet": tweet[:80],
            "true_intent": true_intent,
            "agent_intent": a_res.intent,
            "intent_correct": true_intent == a_res.intent,
            "true_escalation": true_escalation,
            "agent_escalation": is_escalated,
            "esc_correct": true_escalation == is_escalated,
            "agent_reply": (agent_reply_text or "[ESCALATED]")[:100],
            "judge_helpfulness": j_scores["helpfulness"] if j_scores else "",
            "judge_tone": j_scores["tone"] if j_scores else "",
            "judge_accuracy": j_scores["accuracy"] if j_scores else "",
            "judge_conciseness": j_scores["conciseness"] if j_scores else "",
        })
        
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    
    print("\n--- Trivial Baseline ---")
    t_intent = compute_intent_metrics(true_intents, trivial_intents)
    t_esc = compute_escalation_metrics(true_escalations, trivial_escalations)
    print(f"Accuracy: {t_intent['accuracy']:.2%} | Macro F1: {t_intent['macro_f1']:.3f}")
    print(f"Escalation Precision: {t_esc['precision']:.3f} | Recall: {t_esc['recall']:.3f}")
    
    print("\n--- Simple Baseline ---")
    s_intent = compute_intent_metrics(true_intents, simple_intents)
    s_esc = compute_escalation_metrics(true_escalations, simple_escalations)
    print(f"Accuracy: {s_intent['accuracy']:.2%} | Macro F1: {s_intent['macro_f1']:.3f}")
    print(f"Escalation Precision: {s_esc['precision']:.3f} | Recall: {s_esc['recall']:.3f}")
    
    print("\n--- HIVER Agent ---")
    a_intent = compute_intent_metrics(true_intents, agent_intents)
    a_esc = compute_escalation_metrics(true_escalations, agent_escalations)
    print(f"Accuracy: {a_intent['accuracy']:.2%} | Macro F1: {a_intent['macro_f1']:.3f}")
    print(f"Escalation Precision: {a_esc['precision']:.3f} | Recall: {a_esc['recall']:.3f}")
    
    agent_rouge = compute_rouge(retrieved_references, agent_replies)
    print(f"ROUGE-L (vs Retrieved): {agent_rouge:.3f}")
    
    print("\n--- Per-Intent Classification Report ---")
    print(a_intent["report"])
    
    if judge_scores:
        avg_h = sum(s["helpfulness"] for s in judge_scores) / len(judge_scores)
        avg_t = sum(s["tone"] for s in judge_scores) / len(judge_scores)
        avg_a = sum(s["accuracy"] for s in judge_scores) / len(judge_scores)
        avg_c = sum(s["conciseness"] for s in judge_scores) / len(judge_scores)
        print("\n--- LLM Judge Averages (1-5) ---")
        print(f"Helpfulness: {avg_h:.2f} | Tone: {avg_t:.2f} | Accuracy: {avg_a:.2f} | Conciseness: {avg_c:.2f}")
    
    output_path = "tests/evaluation_results.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=detail_rows[0].keys())
        writer.writeheader()
        writer.writerows(detail_rows)
    print(f"\nDetailed per-tweet results saved to: {output_path}")

if __name__ == "__main__":
    run_evaluation("tests/GoldenDataSet.csv", limit=None, use_judge=True)
