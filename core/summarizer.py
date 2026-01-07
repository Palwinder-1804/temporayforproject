from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0  # GPU enabled
)

def summarize_text(text):
    if len(text) < 500:
        return text
    summary = summarizer(
        text,
        max_length=180,
        min_length=80,
        do_sample=False
    )
    return summary[0]["summary_text"]
