from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(text):
    c = canvas.Canvas("audit_report.pdf", pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    text_lines = text.splitlines()
    for i, line in enumerate(text_lines):
        c.drawString(50, height - 80 - (i * 15), line)  # Adjust the vertical spacing as needed
    c.save()
