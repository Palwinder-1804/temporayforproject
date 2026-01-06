def generate_flashcards(summary_text, max_cards=6):
    """
    Converts summary sentences into Q–A flashcards
    """
    sentences = [s.strip() for s in summary_text.split(".") if len(s.strip()) > 10]

    flashcards = []
    for i, sentence in enumerate(sentences[:max_cards]):
        question = f"What is the key idea of point {i + 1}?"
        answer = sentence
        flashcards.append({
            "question": question,
            "answer": answer
        })

    return flashcards
