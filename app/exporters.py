import os
from fpdf import FPDF

class ComicPDF(FPDF):
    """Custom PDF class for comic formatting"""
    
    def header(self):
        """PDF header"""
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'ComicCraft AI - Generated Comic Story', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        """PDF footer with page number"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def save_pdf(layout: list) -> str:
    """Compiles the comic layout into a structured downloadable PDF.
    
    Args:
        layout: List of panel dictionaries with title, image_path, scene_description, narration
        
    Returns:
        Path to the saved PDF file
    """
    os.makedirs("static/exports", exist_ok=True)
    pdf_path = f"static/exports/comic_{os.urandom(4).hex()}.pdf"
    
    try:
        pdf = ComicPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        for panel in layout:
            try:
                pdf.add_page()
                
                # Panel title
                pdf.set_font('Arial', 'B', 12)
                title = panel.get('title', 'Panel')
                pdf.cell(0, 10, title, 0, 1, 'L')
                pdf.ln(3)
                
                # Image
                image_path = panel.get('image_path', '')
                if image_path and os.path.exists(image_path):
                    try:
                        pdf.image(image_path, x=30, y=pdf.get_y(), w=150)
                        pdf.ln(130)
                    except Exception as e:
                        print(f"Warning: Could not add image {image_path}: {str(e)}")
                
                # Scene description
                scene = panel.get('scene_description', '')
                if scene:
                    pdf.set_font('Arial', 'I', 10)
                    pdf.multi_cell(0, 6, f"Scene: {scene}")
                    pdf.ln(3)
                
                # Narration/script
                narration = panel.get('narration', '')
                if narration:
                    pdf.set_font('Arial', '', 10)
                    pdf.multi_cell(0, 6, f"Script: {narration}")
                
                pdf.ln(5)
                
            except Exception as e:
                print(f"Warning: Error processing panel: {str(e)}")
                continue
        
        pdf.output(pdf_path)
        return pdf_path
        
    except Exception as e:
        raise Exception(f"Error generating PDF: {str(e)}")
