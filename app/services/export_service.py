import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def export_anki_csv(flashcards: list[dict]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Front', 'Back'])
    for card in flashcards:
        front = card.get('question', '')
        back = f"{card.get('answer', '')}<br><br><i>Explanation: {card.get('explanation', '')}</i>"
        writer.writerow([front, back])
    return output.getvalue()

def export_printable_pdf(flashcards: list[dict]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    question_style = ParagraphStyle('Question', parent=styles['Heading2'], spaceAfter=6)
    answer_style = ParagraphStyle('Answer', parent=styles['Normal'], spaceAfter=4)
    explanation_style = ParagraphStyle('Explanation', parent=styles['Italic'], spaceAfter=12, textColor='gray')
    
    story = []
    story.append(Paragraph("AI Study Buddy - Study Sheet", styles['Title']))
    story.append(Spacer(1, 20))
    
    for i, card in enumerate(flashcards):
        story.append(Paragraph(f"Q{i+1}: {card.get('question', '')}", question_style))
        story.append(Paragraph(f"A: {card.get('answer', '')}", answer_style))
        story.append(Paragraph(f"Explanation: {card.get('explanation', '')}", explanation_style))
        story.append(Spacer(1, 10))
        
    doc.build(story)
    return buffer.getvalue()
