
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file, preserving paragraphs."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            page_text = page.get_text("text")
            if page_text.strip():
                text += page_text + "\n\n"
        doc.close()

        if not text.strip():
            return "⚠️ No content found in the PDF."
        return text.strip()
    except Exception as e:
        return f"❌ Error extracting PDF text: {e}"


def extract_text_from_url(url):
    """Extracts readable text from a webpage."""
    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, and hidden elements
        for tag in soup(["script", "style", "noscript", "header", "footer", "form", "img", "nav", "aside"]):
            tag.decompose()

        # Extract text from paragraphs and divs
        texts = []
        for element in soup.find_all(["p", "div", "article", "span"]):
            txt = element.get_text(strip=True)
            if txt and len(txt.split()) > 5:  # Only keep meaningful text
                texts.append(txt)

        content = "\n".join(texts)

        print("🔎 Extracted Content Preview:", content[:500])  # Debug log

        return content if content.strip() else "⚠️ No content found."
    except Exception as e:
        print("⚠️ URL extraction error:", e)
        return "⚠️ Could not extract content."
