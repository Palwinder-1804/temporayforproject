import streamlit as st
import tempfile
from multimodal_summarizer import summarize_input
from outputs.flowchart import generate_flowchart
from outputs.flashcards import generate_flashcards

st.set_page_config(
    page_title="Multilingual AI Content Summarizer",
    layout="wide"
)

st.title("🌍 Multilingual AI Content Summarizer")
st.markdown(
    "Upload **text, PDF, image, or video** and get a **summary, flowchart, and flashcards**."
)

# -------------------------
# INPUT SECTION
# -------------------------
st.header("📥 Input")

input_type = st.selectbox(
    "Select input type",
    ["Text", "PDF", "Image", "Video"]
)

text_input = None
file_path = None

if input_type == "Text":
    text_input = st.text_area(
        "Paste your text here",
        height=200
    )

else:
    uploaded_file = st.file_uploader(
        "Upload file",
        type=["pdf", "png", "jpg", "jpeg", "mp4"]
    )

    if uploaded_file:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name

# -------------------------
# PROCESS BUTTON
# -------------------------
if st.button("🚀 Generate Summary"):
    with st.spinner("Processing content..."):
        if input_type == "Text" and text_input:
            summary = summarize_input("text", text_input)

        elif file_path:
            summary = summarize_input(
                input_type.lower(),
                file_path
            )
        else:
            st.warning("Please provide input")
            st.stop()

    # -------------------------
    # OUTPUT SECTION
    # -------------------------
    st.success("Done!")

    st.header("📄 Summary")
    st.write(summary)

    # Flowchart
    st.header("📊 Flowchart")
    flowchart_path = generate_flowchart(summary)
    st.image(flowchart_path)

    # Flashcards
    st.header("🃏 Flashcards")
    flashcards = generate_flashcards(summary)

    for i, card in enumerate(flashcards, 1):
        with st.expander(f"Flashcard {i}"):
            st.markdown(f"**Q:** {card['question']}")
            st.markdown(f"**A:** {card['answer']}")
