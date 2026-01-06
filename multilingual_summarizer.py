import torch
from transformers import pipeline
from langdetect import detect

# ---- DEVICE SETUP ----
device = 0 if torch.cuda.is_available() else -1
print("Using GPU" if device == 0 else "Using CPU")

# ---- MODELS ----
# Translation: any language → English
translator_to_en = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-mul-en",
    device=device
)

# Summarization (English)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=device,
    dtype=torch.float16 if device == 0 else torch.float32
)

def summarize_multilingual(text):
    # Detect language
    lang = detect(text)
    print("Detected language:", lang)

    # Translate to English if needed
    if lang != "en":
        text = translator_to_en(text)[0]["translation_text"]

    # Summarize
    summary = summarizer(
        text,
        max_length=80,
        min_length=30,
        do_sample=False
    )[0]["summary_text"]

    return summary

# ---- TEST INPUT ----
input_text = """
कृत्रिम बुद्धिमत्ता कंप्यूटर विज्ञान की एक शाखा है जो
ऐसी मशीनें बनाने पर केंद्रित है जो मानव जैसी बुद्धि का
प्रदर्शन कर सकें।
"""

print("\nSUMMARY:\n")
print(summarize_multilingual(input_text))
