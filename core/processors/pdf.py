import pdfplumber


def process_pdf(file) -> str:
    """
    Extract and clean text from a PDF file.

    Responsibilities:
    - Read all pages
    - Ignore empty pages
    - Return combined clean text
    """

    if not file:
        return ""

    extracted_text = []

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text)

    except Exception as e:
        # In case pdfplumber fails
        print(f"PDF processing error: {e}")
        return ""

    # Normalize whitespace
    final_text = " ".join(" ".join(extracted_text).split())

    return final_text.strip()
