import re


def clean_text(text: str) -> str:
    """
    Clean and normalize raw text.

    Responsibilities:
    - Remove extra whitespace
    - Normalize line breaks
    - Keep text AI-ready
    """

    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_into_chunks(text: str, max_words: int = 600) -> list[str]:
    """
    Split long text into word-based chunks.

    This prevents transformer models from exceeding token limits.
    """

    if not text:
        return []

    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks
