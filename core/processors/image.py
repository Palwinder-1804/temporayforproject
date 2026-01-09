from PIL import Image
import pytesseract


def process_image(file) -> str:
    """
    Extract text from an image using OCR.

    Responsibilities:
    - Open image safely
    - Perform OCR
    - Normalize text
    """

    if not file:
        return ""

    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)

    except Exception as e:
        print(f"Image processing error: {e}")
        return ""

    # Normalize whitespace
    cleaned_text = " ".join(text.split())

    return cleaned_text.strip()
