import re
from transformers import pipeline
from functools import lru_cache
import torch

from core.summarizer.text_splitter import clean_text, split_into_chunks


# -------------------------------------------------
# Load summarization model (cached)
# -------------------------------------------------
@lru_cache(maxsize=1)
def _load_summarizer():
    # Use GPU if available, otherwise fall back to CPU
    device = 0 if torch.cuda.is_available() else -1
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=device
    )


# -------------------------------------------------
# Summarize a single chunk safely
# -------------------------------------------------
def _summarize_chunk(model, chunk: str) -> str:
    wc = len(chunk.split())

    max_len = min(160, max(70, wc // 2))
    min_len = max(40, max_len // 2)

    result = model(
        chunk,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )

    return result[0]["summary_text"]


# -------------------------------------------------
# Categorize sentences into sections
# -------------------------------------------------
def _categorize_sentences(text: str) -> dict:
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sections = {
        "highlights": [],
        "ideas": [],
        "takeaway": []
    }

    for s in sentences:
        s = s.strip()
        s_lower = s.lower()

        if len(s.split()) < 6:
            continue

        if any(k in s_lower for k in ["transform", "impact", "emerge", "significant"]):
            sections["highlights"].append(s)

        elif any(k in s_lower for k in ["however", "also", "because", "while", "despite"]):
            sections["ideas"].append(s)

        else:
            sections["takeaway"].append(s)

    return sections


# -------------------------------------------------
# MAIN SUMMARY FUNCTION
# -------------------------------------------------
def generate_structured_summary(text: str) -> str:
    """
    Returns a structured summary exactly like the UI example:
    - Key Highlights
    - Main Ideas
    - Purpose / Takeaway
    """

    text = clean_text(text)
    if not text:
        return ""

    chunks = split_into_chunks(text)
    model = _load_summarizer()

    combined_summary = []
    for chunk in chunks:
        combined_summary.append(_summarize_chunk(model, chunk))

    condensed = " ".join(combined_summary)

    sections = _categorize_sentences(condensed)

    # -------------------------------
    # SMART FALLBACK (CRITICAL)
    # -------------------------------
    all_sentences = []
    for v in sections.values():
        all_sentences.extend(v)

    all_sentences = list(dict.fromkeys(all_sentences))

    if not sections["highlights"]:
        sections["highlights"] = all_sentences[:2]

    if not sections["ideas"]:
        sections["ideas"] = all_sentences[2:4]

    if not sections["takeaway"]:
        sections["takeaway"] = all_sentences[-1:]

    # -------------------------------
    # FORMAT OUTPUT (UI-READY)
    # -------------------------------
    output = []

    output.append("📄 Summary\n")

    output.append("🔹 Key Highlights")
    for s in sections["highlights"][:2]:
        output.append(f"• {s}")

    output.append("\n🔹 Main Ideas")
    for s in sections["ideas"][:2]:
        output.append(f"• {s}")

    output.append("\n🔹 Purpose / Takeaway")
    output.append(sections["takeaway"][0])

    return "\n".join(output)
