from inputs.pdf_input import pdf_to_text
from inputs.image_input import image_to_text
from inputs.video_input import video_to_text
from multilingual_summarizer import summarize_multilingual

def summarize_input(input_type, input_path):
    if input_type == "pdf":
        text = pdf_to_text(input_path)
    elif input_type == "image":
        text = image_to_text(input_path)
    elif input_type == "video":
        text = video_to_text(input_path)
    elif input_type == "text":
        text = input_path
    else:
        raise ValueError("Unsupported input type")

    return summarize_multilingual(text)


# ---- TEST ----
if __name__ == "__main__":
    summary = summarize_input(
        input_type="pdf",
        input_path="sample.pdf"
    )
    print("\n📄 SUMMARY:\n")
    print(summary)
