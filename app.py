import streamlit as st
import tempfile

from core.text_processor import clean_text
from core.translator import translate_to_english
from core.summarizer import summarize_text
from core.video_processor import extract_video_text
from core.image_processor import extract_text_from_image
from outputs.flowchart import generate_flowchart
from outputs.flashcards import generate_flashcards

st.set_page_config("AI Content Summarizer", layout="wide")
st.title("🌍 Automated Content Summarizer")

input_type = st.selectbox(
    "Select Input Type",
    ["Text", "Image", "Video"]
)

raw_text = ""

if input_type == "Text":
    raw_text = st.text_area("Paste your content here", height=250)

elif input_type == "Image":
    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if img:
        raw_text = extract_text_from_image(img)

elif input_type == "Video":
    video_url = st.text_input("Enter YouTube video URL")
    if video_url:
        raw_text = extract_video_text(video_url)

if st.button("🚀 Generate Summary") and raw_text:
    with st.spinner("Processing content..."):
        cleaned = clean_text(raw_text)
        translated = translate_to_english(cleaned)
        summary = summarize_text(translated)

    st.subheader("📄 Summary")
    st.write(summary)

    st.subheader("📊 Flowchart")
    st.graphviz_chart(generate_flowchart(summary))

    st.subheader("🃏 Flashcards")
    cards = generate_flashcards(summary)
    for i, card in enumerate(cards, 1):
        st.markdown(f"**Q{i}:** {card['Q']}")
        st.markdown(f"**A{i}:** {card['A']}")
