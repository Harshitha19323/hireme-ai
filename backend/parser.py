import pdfplumber
import io
import re


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract clean text from PDF bytes using pdfplumber."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def clean_text(text: str) -> str:
    """Remove excessive whitespace and normalize text."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def extract_resume_text(file_bytes: bytes, filename: str) -> str:
    """Route to correct extractor based on file type."""
    if filename.lower().endswith(".pdf"):
        raw = extract_text_from_pdf(file_bytes)
    else:
        raw = file_bytes.decode("utf-8", errors="ignore")
    return clean_text(raw)
