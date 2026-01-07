import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=0
    )

def chunk_text(text, chunk_size=800):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

def summarize_text(text):
    summarizer = load_summarizer()

    if len(text.split()) < 300:
        return text

    summaries = []
    for chunk in chunk_text(text):
        out = summarizer(
            chunk,
            max_length=150,
            min_length=60,
            do_sample=False
        )
        summaries.append(out[0]["summary_text"])

    return " ".join(summaries)
