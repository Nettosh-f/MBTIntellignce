#!/usr/bin/env python3
import re
import argparse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PDFGenerator:
    def __init__(self, header_image_path, footer_text, text_file_path, output_path, hebrew_font_path=None):
        """
        Initialize the PDF generator with necessary parameters.
        
        Args:
            header_image_path: Path to the PNG header image
            footer_text: Text to be used as footer
            text_file_path: Path to the text file with content
            output_path: Path where the PDF will be saved
            hebrew_font_path: Path to a Hebrew font file (TTF) for proper rendering
        """
        self.header_image_path = header_image_path
        self.footer_text = footer_text
        self.text_file_path = text_file_path
        self.output_path = output_path
        self.hebrew_font_path = hebrew_font_path
        
        # Register Hebrew font if provided
        if hebrew_font_path:
            try:
                pdfmetrics.registerFont(TTFont('Hebrew', hebrew_font_path))
            except:
                print(f"Warning: Could not register Hebrew font from {hebrew_font_path}")
                print("Using default font instead. Hebrew text may not display correctly.")
        else:
            print("Warning: No Hebrew font provided. Hebrew text may not display correctly.")
            # Try to use a built-in font that might have better Hebrew support
            try:
                pdfmetrics.registerFont(TTFont('Hebrew', "Helvetica"))
            except:
                print("Could not register fallback font. Using system defaults.")
        
        # Set up page size and margins
        self.page_width, self.page_height = letter
        self.margin = 0.75 * inch
        
        # Initialize document and styles
        self.doc = BaseDocTemplate(
            self.output_path,
            pagesize=letter,
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=self.margin + 0.5 * inch,  # Extra space for header
            bottomMargin=self.margin + 0.25 * inch  # Extra space for footer
        )
        
        self.styles = getSampleStyleSheet()
        self.normal_style = self.styles['Normal']
        
        # Create custom style for footer
        self.footer_style = ParagraphStyle(
            'FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER
        )
        
        # Create custom style for Hebrew text (RTL)
        self.hebrew_style = ParagraphStyle(
            'HebrewStyle',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT,
            wordWrap='RTL',
            fontName='Hebrew',
            direction='rtl'
        )

    def _header_footer(self, canvas, doc):
        """
        Add the header and footer to each page.
        """
        # Save canvas state
        canvas.saveState()
        
        # Add header (PNG image)
        try:
            img = Image(self.header_image_path, width=self.page_width - 2*self.margin, height=0.5*inch)
            img.drawOn(canvas, self.margin, self.page_height - self.margin)
        except Exception as e:
            print(f"Error with header image: {e}")
            # Fallback: just write a text header
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(self.margin, self.page_height - self.margin, "HEADER PLACEHOLDER (IMAGE NOT FOUND)")
        
        # Add footer text
        footer = Paragraph(f"{self.footer_text} - Page {doc.page}", self.footer_style)
        footer.wrapOn(canvas, self.page_width - 2*self.margin, 0.25*inch)
        footer.drawOn(canvas, self.margin, 0.5*inch)
        
        # Restore canvas state
        canvas.restoreState()

    def _parse_text_file(self):
        """
        Parse the input text file and split the content by page markers.
        
        Returns:
            List of tuples (text_content, company_name) for each page
        """
        try:
            with open(self.text_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extract company names and pages
            # Pattern 1: Find all page markers with page numbers
            page_markers = re.finditer(r'---page\s+(\d+)\s+---', content)
            
            # Get the positions of all markers
            marker_positions = [(m.group(0), m.start(), m.end()) for m in page_markers]
            
            pages = []
            
            # Handle content before the first marker if any
            if marker_positions and marker_positions[0][1] > 0:
                pages.append((content[:marker_positions[0][1]].strip(), ""))
            
            # Extract content between markers
            for i in range(len(marker_positions)):
                start_pos = marker_positions[i][2]
                end_pos = marker_positions[i+1][1] if i+1 < len(marker_positions) else len(content)
                
                page_content = content[start_pos:end_pos].strip()
                
                # Try to extract company name (assuming it's the first line or a specially marked line)
                lines = page_content.split('\n')
                company_name = ""
                
                if lines and lines[0].strip() and not lines[0].startswith("---"):
                    # Assume first non-empty line that's not a marker is a company name
                    company_name = lines[0].strip()
                    # Remove company name from content to process rest as Hebrew
                    page_content = '\n'.join(lines[1:]).strip()
                
                pages.append((page_content, company_name))
            
            return pages
        except Exception as e:
            print(f"Error parsing text file: {e}")
            return ["Error loading content from text file."]

    def generate_pdf(self):
        """
        Generate the PDF with the specified header, footer, and content.
        """
        # Get page content
        pages_content = self._parse_text_file()
        
        # Create page template with header and footer
        frame = Frame(
            self.margin, 
            self.margin + 0.25*inch,  # Bottom margin (allow space for footer)
            self.page_width - 2*self.margin,
            self.page_height - 2*self.margin - 0.75*inch,  # Top and bottom margins with header/footer
            id='normal'
        )
        
        template = PageTemplate(
            id='template',
            frames=[frame],
            onPage=self._header_footer
        )
        
        self.doc.addPageTemplates([template])
        
        # Build document content
        story = []
        
        for page_content, company_name in pages_content:
            if page_content.strip() or company_name.strip():  # Skip empty pages
                # Add company name if it exists (left-to-right)
                if company_name.strip():
                    company_para = Paragraph(company_name, self.styles['Heading2'])
                    story.append(company_para)
                    story.append(Spacer(1, 0.2*inch))
                
                # Add Hebrew content with RTL formatting
                if page_content.strip():
                    paragraphs = page_content.split('\n\n')
                    
                    for para in paragraphs:
                        if para.strip():
                            # Use RTL Hebrew style for paragraphs
                            p = Paragraph(para.replace('\n', '<br/>'), self.hebrew_style)
                            story.append(p)
                            story.append(Spacer(1, 0.1*inch))
                
                # Add page break between pages from the text file
                # (except after the last page)
                if (page_content, company_name) != pages_content[-1]:
                    story.append(Spacer(1, 0.1*inch))
                    story.append(PageBreak())
        
        # Build the PDF
        self.doc.build(story)
        print(f"PDF generated successfully at: {self.output_path}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a PDF with custom header and footer.')
    parser.add_argument('--header', required=True, help='Path to PNG header image')
    parser.add_argument('--footer', required=True, help='Text for footer')
    parser.add_argument('--text', required=True, help='Path to text file with content')
    parser.add_argument('--output', required=True, help='Output PDF file path')
    parser.add_argument('--hebrew-font', help='Path to Hebrew TTF font file for proper RTL rendering')
    
    args = parser.parse_args()
    
    # Create and generate PDF
    pdf_gen = PDFGenerator(
        header_image_path=args.header,
        footer_text=args.footer,
        text_file_path=args.text,
        output_path=args.output,
        hebrew_font_path=args.hebrew_font
    )
    
    pdf_gen.generate_pdf()
