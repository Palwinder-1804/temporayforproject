import re
from transformers import pipeline
from functools import lru_cache


# -------------------------------------------------
# Load Question Generation model (cached)
# -------------------------------------------------
@lru_cache(maxsize=1)
def _load_qg_model():
    return pipeline(
        "text2text-generation",
        model="valhalla/t5-small-qg-prepend",
        device=0  # set -1 for CPU
    )


# -------------------------------------------------
# Split text into candidate sentences
# -------------------------------------------------
def _split_into_sentences(text: str) -> list[str]:
    return [
        s.strip()
        for s in re.split(r'(?<=[.!?])\s+', text)
        if len(s.split()) > 7
    ]


# -------------------------------------------------
# MAIN FLASHCARD GENERATOR
# -------------------------------------------------
def generate_flashcards(text: str, max_cards: int = 6) -> list[dict]:
    """
    Generate Q/A based flashcards.

    Returns:
    [
        { "question": "...", "answer": "..." }
    ]
    """

    if not text:
        return []

    model = _load_qg_model()
    sentences = _split_into_sentences(text)

    flashcards = []

    for sentence in sentences:
        prompt = f"generate question: {sentence}"

        try:
            output = model(
                prompt,
                max_new_tokens=48,
                do_sample=False
            )

            question = output[0]["generated_text"]
            question = question.replace("question:", "").strip()

            # Filter weak questions
            if len(question.split()) < 4:
                continue

            flashcards.append({
                "question": question,
                "answer": sentence
            })

            if len(flashcards) >= max_cards:
                break

        except Exception as e:
            print(f"Flashcard error: {e}")
            continue

    return flashcards
