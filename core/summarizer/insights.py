import re
from collections import Counter


def extract_keywords(text: str, top_k: int = 6) -> list[str]:
    """
    Extract important keywords from text.
    Simple frequency-based approach (fast & reliable).
    """

    if not text:
        return []

    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())

    stopwords = {
        "this", "that", "with", "from", "have", "were",
        "which", "will", "their", "about", "there"
    }

    filtered = [w for w in words if w not in stopwords]

    most_common = Counter(filtered).most_common(top_k)

    return [word for word, _ in most_common]


def extract_themes(text: str) -> list[str]:
    """
    Extract high-level themes from text.
    """

    if not text:
        return []

    themes = []

    if "challenge" in text.lower():
        themes.append("Challenges")

    if "benefit" in text.lower() or "advantage" in text.lower():
        themes.append("Benefits")

    if "future" in text.lower():
        themes.append("Future Outlook")

    if "risk" in text.lower():
        themes.append("Risks")

    return themes


def generate_insights(text: str) -> dict:
    """
    Generate a compact insights object.
    """

    return {
        "keywords": extract_keywords(text),
        "themes": extract_themes(text)
    }
