from ..utils.blocklist_loader import get_blocklist
from ..utils.normalization import Normalization
from rapidfuzz import fuzz

def fuzzy_match(token: str, keyword: str, threshold: int = 80) -> bool:
    if token == keyword:
        return True
    if len(token) < 3:
        return False
    return fuzz.partial_ratio(token, keyword) >= threshold

def analyze(user_input: str) -> dict:
    normalizer = Normalization()
    tokens = normalizer.normalize_content(user_input)
    blocklist = get_blocklist()["categories"]

    matched_categories = []
    matched_words = []

    for category, meta in blocklist.items():
        for keyword in meta['keywords']:
            for token in tokens:
                if fuzzy_match(token, keyword):
                    matched_categories.append(category)
                    matched_words.append(keyword)

    return {
        "violation": bool(matched_categories),
        "harm_type": list(set(matched_categories)),
        "severity": max([blocklist[cat]["severity"] for cat in matched_categories], default="none"),
        "reasoning": f"Matched words: {matched_words}" if matched_words else 'No matches found'
    }