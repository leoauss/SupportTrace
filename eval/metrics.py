import warnings
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
from rouge_score import rouge_scorer

def compute_intent_metrics(y_true: list[str], y_pred: list[str]) -> dict:
    """Computes evaluation metrics for intent classification."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
            "report": classification_report(y_true, y_pred, zero_division=0)
        }

def compute_escalation_metrics(y_true: list[bool], y_pred: list[bool]) -> dict:
    """Computes precision and recall for escalation routing (True = escalate)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return {
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
        }

def compute_rouge(references: list[str], predictions: list[str]) -> float:
    """
    Computes average ROUGE-L f-measure across the dataset.
    Expects lists of strings. 
    """
    if not references or not predictions:
        return 0.0
        
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    
    total_f1 = 0.0
    valid_pairs = 0
    
    for ref, pred in zip(references, predictions):
        if isinstance(ref, str) and isinstance(pred, str) and ref.strip() and pred.strip():
            score = scorer.score(ref, pred)["rougeL"].fmeasure
            total_f1 += score
            valid_pairs += 1
            
    if valid_pairs == 0:
        return 0.0
        
    return total_f1 / valid_pairs
