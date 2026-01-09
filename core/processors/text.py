def process_text(text: str) -> str:
    """
    Process plain text input.

    Responsibilities:
    - Validate input
    - Normalize whitespace
    - Return clean text for downstream AI tasks
    """

    if not text:
        return ""

    # Normalize whitespace
    cleaned_text = " ".join(text.split())

    return cleaned_text.strip()
