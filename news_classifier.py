import re

class NewsClassifier:
    def __init__(self):
        # Common words found in news articles
        self.keywords = [
            "news", "breaking", "report", "reported", "update", "published",
            "via reuters", "via ap", "said", "announced", "journal",
            "bbc", "cnn", "times", "guardian", "press release", "headlines"
        ]

    def clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text or "").strip().lower()
        return text

    def is_news(self, text: str, threshold: float = 0.0) -> bool:
        if not text.strip():
            return False
        cleaned = self.clean_text(text)
        return any(k in cleaned for k in self.keywords)

    def classify(self, text: str):
        if self.is_news(text):
            return "news", 1.0
        return "not news", 0.0


