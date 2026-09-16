import json
import scipy.stats as stats
from sklearn.metrics import cohen_kappa_score
from eval.llm_judge import LLMJudge

def compute_calibration(human_scores_file: str):
    """
    Reads a JSON file containing 50 human-graded examples.
    Expected format per example:
    {
        "tweet": "...",
        "reply": "...",
        "human_helpfulness": 4,
        "human_tone": 5,
        "human_accuracy": 5,
        "human_conciseness": 3
    }
    """
    with open(human_scores_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    judge = LLMJudge()
    all_human_scores = []
    all_llm_scores = []
    
    print(f"Calibrating LLM Judge against {len(data)} human-scored examples...")
    
    for i, item in enumerate(data):
        print(f"Scoring example {i+1}/{len(data)}...")
        llm_scores = judge.score(item["tweet"], item["reply"])
        
        all_human_scores.extend([
            item["human_helpfulness"],
            item["human_tone"],
            item["human_accuracy"],
            item["human_conciseness"]
        ])
        
        all_llm_scores.extend([
            llm_scores.get("helpfulness", 0),
            llm_scores.get("tone", 0),
            llm_scores.get("accuracy", 0),
            llm_scores.get("conciseness", 0)
        ])
        
        # Print discrepancies
        discrepancy = False
        metrics = ["helpfulness", "tone", "accuracy", "conciseness"]
        for m in metrics:
            h = item[f"human_{m}"]
            l = llm_scores.get(m, 0)
            if abs(h - l) >= 2:
                if not discrepancy:
                    print(f"\n--- Discrepancy on Example {i+1} ---")
                    print(f"Reply: {item['reply']}")
                    discrepancy = True
                print(f"  {m.capitalize()}: Human={h} | LLM={l}")

        
    pearson_corr, p_value = stats.pearsonr(all_human_scores, all_llm_scores)
    
    kappa = cohen_kappa_score(all_human_scores, all_llm_scores)
    
    print("\n--- Calibration Results ---")
    print(f"Pearson Correlation: {pearson_corr:.3f} (p={p_value:.3e})")
    print(f"Cohen's Kappa:       {kappa:.3f}")
    
    if pearson_corr > 0.7:
        print("Verdict: STRONG agreement! The LLM Judge is highly calibrated.")
    elif pearson_corr > 0.5:
        print("Verdict: MODERATE agreement. Consider refining your rubric.")
    else:
        print("Verdict: POOR agreement. You MUST revise your rubric before using this judge.")

if __name__ == "__main__":
    try:
        compute_calibration("data/human_calibration.json")
    except FileNotFoundError:
        print("Please create 'data/human_calibration.json' with your 50 human scores first!")
