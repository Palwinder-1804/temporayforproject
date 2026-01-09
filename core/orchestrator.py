from core.processors.pdf import process_pdf
from core.processors.image import process_image
from core.processors.video import process_video

from core.summarizer.summary_engine import generate_structured_summary
from core.flashcards.generator import generate_flashcards
from core.flowchart.generator import generate_flowchart
from core.summarizer.insights import generate_insights


def process_text(text: str) -> str:
    """Clean raw text input."""
    if not text:
        return ""
    return text.strip()


def run_pipeline(
    *,
    input_type: str,
    text: str = None,
    file=None,
    url: str = None
) -> dict:

    # ----------------------------
    # STEP 1: Extract raw text
    # ----------------------------
    if input_type == "text":
        raw_text = process_text(text)

    elif input_type == "pdf":
        raw_text = process_pdf(file)

    elif input_type == "image":
        raw_text = process_image(file)

    elif input_type == "video":
        raw_text = process_video(url)

    else:
        return {
            "summary": "",
            "insights": {},
            "flashcards": [],
            "flowchart": ""
        }

    if not raw_text:
        return {
            "summary": "No text could be extracted.",
            "insights": {},
            "flashcards": [],
            "flowchart": ""
        }

    # ----------------------------
    # STEP 2: AI generation
    # ----------------------------
    try:
        summary = generate_structured_summary(raw_text)
        insights = generate_insights(raw_text)
        flashcards = generate_flashcards(raw_text)
        flowchart = generate_flowchart(raw_text)
    except Exception as e:
        print("Pipeline error:", e, flush=True)
        return {
            "error": str(e),
            "summary": "",
            "insights": {},
            "flashcards": [],
            "flowchart": ""
        }

    # ----------------------------
    # STEP 3: Return JSON-safe data
    # ----------------------------
    return {
        "summary": summary,
        "insights": insights,
        "flashcards": flashcards,
        "flowchart": flowchart
    }
