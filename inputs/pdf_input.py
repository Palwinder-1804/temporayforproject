import fitz  # PyMuPDF

def pdf_to_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text
