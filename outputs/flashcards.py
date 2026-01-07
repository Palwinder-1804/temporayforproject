def generate_flashcards(summary):
    sentences = summary.split(".")[:5]
    flashcards = []

    for s in sentences:
        flashcards.append({
            "Q": "Explain this point",
            "A": s.strip()
        })

    return flashcards
