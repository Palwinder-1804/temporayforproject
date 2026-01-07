import fitz

def pdf_to_text(path: str) -> str:
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text
