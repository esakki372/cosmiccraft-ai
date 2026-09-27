import os
from fpdf import FPDF

class ComicPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'ComicCraft AI - Generated Comic Story', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def save_pdf(layout: list) -> str:
    """Compiles the comic layout into a structured downloadable PDF."""
    os.makedirs("static/exports", exist_ok=True)
    pdf_path = f"static/exports/comic_{os.urandom(4).hex()}.pdf"
    
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for panel in layout:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, panel['title'], 0, 1, 'L')
        
        if panel['image_path'] and os.path.exists(panel['image_path']):
            pdf.image(panel['image_path'], x=30, y=25, w=150)
            pdf.ln(130)
            
        pdf.set_font('Arial', 'I', 10)
        pdf.multi_cell(0, 6, f"Scene: {panel['scene_description']}")
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, f"Script: {panel['narration']}")
        
    pdf.output(pdf_path)
    return pdf_path