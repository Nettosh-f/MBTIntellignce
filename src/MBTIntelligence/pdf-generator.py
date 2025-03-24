import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display as bidialg
from arabic_reshaper.arabic_reshaper import reshape
# from arabic_reshaper.constants import DONT_RESIZE


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
        if hebrew_font_path and os.path.exists(hebrew_font_path):
            try:
                pdfmetrics.registerFont(TTFont('Hebrew', hebrew_font_path))
                print(f"Successfully registered Hebrew font from {hebrew_font_path}")
            except Exception as e:
                print(f"Warning: Could not register Hebrew font from {hebrew_font_path}: {e}")
                print("Using default font instead. Hebrew text may not display correctly.")
        else:
            print(f"Warning: Hebrew font file not found at {hebrew_font_path}")
            print("Using default font instead. Hebrew text may not display correctly.")

        # Fall back to a default font if needed
        if not hebrew_font_path or not os.path.exists(hebrew_font_path):
            print("Using Helvetica as fallback font")

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
            fontName='Hebrew' if hebrew_font_path and os.path.exists(hebrew_font_path) else 'Helvetica',
            fontSize=10,
            direction='rtl'
        )

    def _header_footer(self, canvas, doc):
        """
        Add the header and footer to each page.
        """
        # Save canvas state
        canvas.saveState()

        # Add header (PNG image)
        if os.path.exists(self.header_image_path):
            try:
                img = Image(self.header_image_path, width=self.page_width - 2 * self.margin, height=0.5 * inch)
                img.drawOn(canvas, self.margin, self.page_height - self.margin)
            except Exception as e:
                print(f"Error with header image: {e}")
                # Fallback: just write a text header
                canvas.setFont('Helvetica-Bold', 12)
                canvas.drawString(self.margin, self.page_height - self.margin, "HEADER PLACEHOLDER (IMAGE ERROR)")
        else:
            print(f"Header image not found at: {self.header_image_path}")
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(self.margin, self.page_height - self.margin, "HEADER PLACEHOLDER (IMAGE NOT FOUND)")

        # Add footer text
        footer = Paragraph(f"{self.footer_text} - Page {doc.page}", self.footer_style)
        footer.wrapOn(canvas, self.page_width - 2 * self.margin, 0.25 * inch)
        footer.drawOn(canvas, self.margin, 0.5 * inch)

        # Restore canvas state
        canvas.restoreState()

    def _parse_text_file(self):
        """
        Parse the input text file and split the content by page markers.

        Returns:
            List of tuples (text_content, company_name) for each page
        """
        if not os.path.exists(self.text_file_path):
            print(f"ERROR: Text file not found at: {self.text_file_path}")
            # Return a default page so PDF doesn't end up empty
            return [("Text file not found. Please check the path.", "Error")]

        try:
            with open(self.text_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            print(f"Successfully read text file. Length: {len(content)} characters")

            # DEBUG: Print the first 200 characters to verify content
            print(f"First 200 characters of content: {content[:200]}")

            # Extract page markers
            page_markers = list(re.finditer(r'---\s*\{\s*}\s*---', content))
            print(f"Found {len(page_markers)} page markers in the text")

            # If no page markers found, treat the entire file as one page
            if not page_markers:
                print("No page markers found. Treating entire file as one page.")
                return [(content, "")]

            # Get the positions of all markers
            marker_positions = [(m.group(0), m.start(), m.end()) for m in page_markers]

            pages = []

            # Handle content before the first marker if any
            if marker_positions and marker_positions[0][1] > 0:
                first_content = content[:marker_positions[0][1]].strip()
                if first_content:
                    print(f"Adding content before first page marker ({len(first_content)} chars)")
                    pages.append((first_content, ""))

            for i in range(len(marker_positions)):
                start_pos = marker_positions[i][2]
                end_pos = marker_positions[i + 1][1] if i + 1 < len(marker_positions) else len(content)

                page_content = content[start_pos:end_pos].strip()

                # Only process non-empty content
                if page_content:
                    # Try to extract company name (assuming it's the first line)
                    lines = page_content.split('\n')
                    company_name = ""

                    if lines and lines[0].strip() and not lines[0].startswith("---"):
                        # Assume first non-empty line that's not a marker is a company name
                        company_name = lines[0].strip()
                        # Remove company name from content to process rest as Hebrew
                        page_content = '\n'.join(lines[1:]).strip()

                    # Use bidialg.get_display to handle bidirectional text
                    reshaped_content = bidialg.get_display(page_content)

                    print(
                        f"Adding page {i + 1} with company name: '{company_name}' and content length: {len(reshaped_content)}")
                    pages.append((reshaped_content, company_name))

            # If we still have no pages, add a fallback
            if not pages:
                print("WARNING: No content pages were extracted. Adding fallback page.")
                pages.append(("No content pages were found to add to the PDF.", "Error"))

            print(f"Total pages extracted: {len(pages)}")
            return pages

        except Exception as e:
            print(f"Error parsing text file: {e}")
            # Return a default page so PDF doesn't end up empty
            return [("Error loading content from text file: " + str(e), "Error")]

    def generate_pdf(self):
        """
        Generate the PDF with the specified header, footer, and content.
        """
        # Get page content
        pages_content = self._parse_text_file()

        if not pages_content:
            print("ERROR: No content pages to add to PDF")
            # Add a default page to avoid empty PDF
            pages_content = [("No content was found to add to the PDF.", "Error")]

        # Create page template with header and footer
        frame = Frame(
            self.margin,
            self.margin + 0.25 * inch,  # Bottom margin (allow space for footer)
            self.page_width - 2 * self.margin,
            self.page_height - 2 * self.margin - 0.75 * inch,  # Top and bottom margins with header/footer
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

        print(f"Building PDF with {len(pages_content)} pages")

        for page_num, (page_content, company_name) in enumerate(pages_content, 1):
            print(f"Processing page {page_num}: Company: '{company_name}', Content length: {len(page_content)}")

            if page_content.strip() or company_name.strip():  # Skip empty pages
                # Add company name as a separate paragraph
                company_paragraph = Paragraph(company_name, self.normal_style)
                story.append(company_paragraph)

                # Add Hebrew text as a separate paragraph
                # Use arabic_reshaper to reshape Hebrew text
                reshaped_content = reshape(page_content)
                hebrew_paragraph = Paragraph(reshaped_content, self.hebrew_style)
                story.append(hebrew_paragraph)

                # Add a page break after each page except the last one
                if page_num < len(pages_content):
                    story.append(PageBreak())

        self.doc.build(story)

        print("PDF generation completed successfully at")


# Main execution code
if __name__ == "__main__":
    header_image_path = r"F:\projects\MBTInteligence\media\full_logo.png"
    footer_text = "created by Netta Ben Sinai"
    text_file_path = r"F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI_cleaned_hebrew.txt"
    output_path = r"F:\projects\MBTInteligence\output\nir-bensinai-MBTI_cleaned_hebrew.pdf"
    hebrew_font_path = r"F:\projects\MBTInteligence\media\fonts\FrankRuhlLibre-VariableFont_wght.ttf"

    # Check path existence before creating the PDF
    print(f"Checking paths:")
    print(f"Header image: {'EXISTS' if os.path.exists(header_image_path) else 'NOT FOUND'}")
    print(f"Text file: {'EXISTS' if os.path.exists(text_file_path) else 'NOT FOUND'}")
    print(f"Hebrew font: {'EXISTS' if os.path.exists(hebrew_font_path) else 'NOT FOUND'}")

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

    # Create PDF generator and generate PDF
    pdf_gen = PDFGenerator(
        header_image_path=header_image_path,
        footer_text=footer_text,
        text_file_path=text_file_path,
        output_path=output_path,
        hebrew_font_path=hebrew_font_path
    )
    print("PDF generation started...")
    pdf_gen.generate_pdf()
    print(f"PDF generated at {output_path}")