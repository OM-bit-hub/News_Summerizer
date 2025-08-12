from rouge_score import rouge_scorer
import bert_score
from typing import Dict

class SummaryEvaluator:
    def __init__(self, lang_code: str = "en"):
        """
        lang_code: language code for BERTScore (e.g. "en", "hi", "mr")
        """
        self.rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.lang_code = (lang_code or "en")

    def evaluate_rouge(self, summary: str, reference: str) -> Dict[str, float]:
        try:
            scores = self.rouge.score(reference or "", summary or "")
            return {
                "rouge1": float(scores["rouge1"].fmeasure),
                "rouge2": float(scores["rouge2"].fmeasure),
                "rougeL": float(scores["rougeL"].fmeasure),
            }
        except Exception:
            return {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}

    def evaluate_bertscore(self, summary: str, reference: str) -> Dict[str, float]:
        try:
            P, R, F1 = bert_score.score([summary or ""], [reference or ""], lang=self.lang_code, rescale_with_baseline=True)
            return {"bertscore_f1": float(F1[0].item())}
        except Exception:
            return {"bertscore_f1": 0.0}

    def evaluate_all(self, summaries: dict, reference: str) -> dict:
        """
        summaries: {"cohere": "...", "t5": "..."} typically english summaries
        """
        results = {}
        for name, summary in (summaries or {}).items():
            rouge_scores = self.evaluate_rouge(summary, reference)
            bert_scores = self.evaluate_bertscore(summary, reference)
            combined = {**rouge_scores, **bert_scores}
            results[name] = combined
        return results

    def select_best_summary(self, scores: dict) -> str:
        """
        Selects the model with highest sum(rouge1 + rouge2 + rougeL + bertsccore_f1)
        """
        if not scores:
            return None
        def score_sum(metric_dict):
            return (metric_dict.get('rouge1', 0.0) +
                    metric_dict.get('rouge2', 0.0) +
                    metric_dict.get('rougeL', 0.0) +
                    metric_dict.get('bertscore_f1', 0.0))
        best_model = max(scores.items(), key=lambda x: score_sum(x[1]))[0]
        return best_model
