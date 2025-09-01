
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os
import markdown
from bs4 import BeautifulSoup

def markdown_to_plain_text(md_text):
    """Convert markdown to plain text for PDF."""
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def generate_pdf(summary, image_path=None):
    pdf_path = "summary.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    plain_summary = markdown_to_plain_text(summary)
    elements.append(Paragraph("<b>AI Generated Summary:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(plain_summary, styles["Normal"]))
    elements.append(Spacer(1, 20))

    if image_path and os.path.exists(image_path):
        elements.append(Paragraph("<b>Generated Image:</b>", styles["Heading2"]))
        elements.append(Spacer(1, 12))
        elements.append(Image(image_path, width=400, height=300))
        elements.append(Spacer(1, 20))

    doc.build(elements)
    return pdf_path
