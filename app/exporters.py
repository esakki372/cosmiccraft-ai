import os
from fpdf import FPDF

class ComicPDF(FPDF):
    """Custom PDF class for comic formatting"""
    
    def header(self):
        """PDF header"""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'ComicCraft AI - Generated Comic', 0, 1, 'C')
        self.ln(3)

    def footer(self):
        """PDF footer with page number"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def save_pdf(layout: list) -> str:
    """Compiles the comic layout into a structured downloadable PDF.
    
    Args:
        layout: List of panel dictionaries
        
    Returns:
        Path to the saved PDF file
    """
    os.makedirs("static/exports", exist_ok=True)
    pdf_path = f"static/exports/comic_{os.urandom(4).hex()}.pdf"
    
    try:
        pdf = ComicPDF()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()
        
        for i, panel in enumerate(layout):
            try:
                # Panel title
                pdf.set_font('Arial', 'B', 11)
                title = panel.get('title', 'Panel')
                pdf.cell(0, 8, title, 0, 1, 'L')
                pdf.ln(2)
                
                # Image
                image_path = panel.get('image_path', '')
                if image_path and os.path.exists(image_path):
                    try:
                        pdf.image(image_path, x=20, y=pdf.get_y(), w=170)
                        pdf.ln(100)
                    except Exception as e:
                        pdf.set_font('Arial', '', 9)
                        pdf.cell(0, 5, f"[Image: {image_path}]", 0, 1)
                
                # Narration
                narration = panel.get('narration', '')
                if narration:
                    pdf.set_font('Arial', '', 9)
                    text_short = narration[:200] if len(narration) > 200 else narration
                    pdf.multi_cell(0, 4, text_short)
                
                pdf.ln(3)
                
                # Add page break after each panel except last
                if i < len(layout) - 1:
                    pdf.add_page()
                    
            except Exception as e:
                print(f"Warning: Error processing panel {i}: {str(e)}")
                continue
        
        pdf.output(pdf_path)
        return pdf_path
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return ""
