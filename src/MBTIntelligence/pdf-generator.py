import os
import re
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, PageTemplate, BaseDocTemplate, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import Spacer, Image, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from bidi.algorithm import get_display as bidialg
from arabic_reshaper import reshape
from utils import find_type, get_date, get_name

MBTI_type = find_type(r"F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI-cleaned-hebrew.txt")
MBTI_name = get_name(r"F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI-cleaned-hebrew.txt")
MBTI_date = get_date(r"F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI-cleaned-hebrew.txt")


class PDFGenerator:
    def __init__(self, header_image_path, footer_text, text_file_path, output_path,
                 hebrew_font_path=None, fixed_text=None, page_size=letter,
                 background_color=None, margins=None, page_template=None):
        """
        Initialize the PDF generator with necessary parameters.

        Args:
            header_image_path: Path to the PNG header image
            footer_text: Text to be used as footer
            text_file_path: Path to the text file with content
            output_path: Path where the PDF will be saved
            hebrew_font_path: Path to a Hebrew font file (TTF) for proper rendering
            fixed_text: Dictionary mapping page numbers to fixed text to insert
                        Format: {page_number: {"text": "content", "position": "top|bottom|after_company",
                                              "alignment": "left|right|center", "line_alignments": [list of alignment per line],
                                              "line_styles": [list of style names per line]}}
            page_size: ReportLab page size (letter, A4, etc.)
            background_color: Color of the page background (reportlab.lib.colors)
            margins: Dictionary with margin settings {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75} in inches
            page_template: Optional custom page template name ('default', 'fancy', etc.)
        """
        self.header_image_path = header_image_path
        self.footer_text = footer_text
        self.text_file_path = text_file_path
        self.output_path = output_path
        self.hebrew_font_path = hebrew_font_path
        self.fixed_text = fixed_text or {}
        self.page_size = page_size
        self.background_color = background_color

        # Set default margins if not provided
        if margins is None:
            self.margins = {
                'left': 0.75,
                'right': 0.75,
                'top': 1.25,  # Extra space for header
                'bottom': 1.0  # Extra space for footer
            }
        else:
            self.margins = margins

        self.page_template = page_template or 'default'

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

        # Set up page size and margins
        self.page_width, self.page_height = self.page_size
        self.margin_left = self.margins['left'] * inch
        self.margin_right = self.margins['right'] * inch
        self.margin_top = self.margins['top'] * inch
        self.margin_bottom = self.margins['bottom'] * inch

        # Initialize document and styles
        self.doc = BaseDocTemplate(
            self.output_path,
            pagesize=self.page_size,
            leftMargin=self.margin_left,
            rightMargin=self.margin_right,
            topMargin=self.margin_top,
            bottomMargin=self.margin_bottom
        )

        self.styles = getSampleStyleSheet()
        self.normal_style = self.styles['Normal']

        # Create various text styles
        self._create_styles()

    def _create_styles(self):
        """Create all the paragraph styles needed for the document"""
        # Base font settings
        hebrew_font = 'Hebrew' if self.hebrew_font_path and os.path.exists(self.hebrew_font_path) else 'Helvetica'

        # Create custom style for footer
        self.footer_style = ParagraphStyle(
            'FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            fontName=hebrew_font
        )

        # Style for Hebrew text (RTL)
        self.hebrew_style = ParagraphStyle(
            'HebrewStyle',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT,
            fontName=hebrew_font,
            fontSize=10,
            direction='rtl'
        )

        # Style for fixed text - right aligned (default for Hebrew)
        self.fixed_text_style = ParagraphStyle(
            'FixedTextStyle',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT,
            fontName=hebrew_font,
            fontSize=10,
            direction='rtl',
        )

        # Style for centered text
        self.centered_text_style = ParagraphStyle(
            'CenteredTextStyle',
            parent=self.styles['Normal'],
            alignment=TA_CENTER,
            fontName=hebrew_font,
            fontSize=10,
            direction='rtl',
        )

        # Style for left-aligned text (would be good for English or numbers)
        self.left_text_style = ParagraphStyle(
            'LeftTextStyle',
            parent=self.styles['Normal'],
            alignment=TA_LEFT,
            fontName=hebrew_font,
            fontSize=10,
        )

        # Title style (large, bold, centered)
        self.title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            alignment=TA_CENTER,
            fontName=hebrew_font,
            fontSize=16,
            spaceAfter=12,
            spaceBefore=12,
            direction='rtl',
            textColor=colors.darkblue
        )

        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=self.styles['Heading2'],
            alignment=TA_RIGHT,
            fontName=hebrew_font,
            fontSize=14,
            spaceAfter=10,
            spaceBefore=10,
            direction='rtl',
            textColor=colors.darkblue
        )

        # Bold style
        self.bold_style = ParagraphStyle(
            'BoldStyle',
            parent=self.hebrew_style,
            fontName=hebrew_font,  # Just use the base font since we can't easily check for bold variant
            fontSize=10,
            direction='rtl',
            fontWeight='bold'  # Try to make it bold this way
        )

        # Italic style
        self.italic_style = ParagraphStyle(
            'ItalicStyle',
            parent=self.hebrew_style,
            fontName=hebrew_font,  # Just use the base font
            fontSize=10,
            direction='rtl',
            textColor=colors.darkslategray,
            fontSlant='italic'  # Try to make it italic this way
        )

        # Quote style (indented, italic)
        self.quote_style = ParagraphStyle(
            'QuoteStyle',
            parent=self.hebrew_style,
            leftIndent=20,
            rightIndent=20,
            fontName=hebrew_font,
            fontSize=10,
            textColor=colors.darkslategray,
            direction='rtl',
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5,
            borderRadius=5,
            backColor=colors.whitesmoke,
            fontSlant='italic'  # Try to make it italic this way
        )

    def _header_footer(self, canvas, doc):
        """
        Add the header and footer to each page.
        """
        # Save canvas state
        canvas.saveState()

        # Add background color if specified
        if self.background_color:
            canvas.setFillColor(self.background_color)
            canvas.rect(0, 0, self.page_width, self.page_height, fill=1, stroke=0)

        # Draw decorative elements based on template
        if self.page_template == 'fancy':
            # Draw a top border
            canvas.setStrokeColor(colors.darkblue)
            canvas.setLineWidth(2)
            canvas.line(self.margin_left, self.page_height - 0.5 * inch,
                        self.page_width - self.margin_right, self.page_height - 0.5 * inch)

            # Draw a bottom border
            canvas.line(self.margin_left, 0.5 * inch,
                        self.page_width - self.margin_right, 0.5 * inch)

        elif self.page_template == 'watermark':
            # Add a watermark
            canvas.setFont('Helvetica', 60)
            canvas.setFillColor(colors.lightgrey.clone(alpha=0.3))
            canvas.saveState()
            canvas.translate(self.page_width / 2, self.page_height / 2)
            canvas.rotate(45)
            canvas.drawCentredString(0, 0, "DRAFT")
            canvas.restoreState()

        # Add header (PNG image)
        if os.path.exists(self.header_image_path):
            try:
                img = Image(self.header_image_path, width=self.page_width - 2 * self.margin_left, height=0.5 * inch)
                img.drawOn(canvas, self.margin_left, self.page_height - self.margin_top + 0.25 * inch)
            except Exception as e:
                print(f"Error with header image: {e}")
                # Fallback: just write a text header
                canvas.setFont('Helvetica-Bold', 12)
                canvas.drawString(self.margin_left, self.page_height - self.margin_top + 0.25 * inch,
                                  "HEADER PLACEHOLDER (IMAGE ERROR)")
        else:
            print(f"Header image not found at: {self.header_image_path}")
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(self.margin_left, self.page_height - self.margin_top + 0.25 * inch,
                              "HEADER PLACEHOLDER (IMAGE NOT FOUND)")

        # Add footer text
        footer = Paragraph(f"{self.footer_text} - Page {doc.page}", self.footer_style)
        footer.wrapOn(canvas, self.page_width - 2 * self.margin_left, 0.25 * inch)
        footer.drawOn(canvas, self.margin_left, 0.5 * inch)

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

            # Extract page markers using the pattern --- עמוד # ---
            page_markers = list(re.finditer(r'---\s*עמוד\s*\d+\s*---', content))
            print(f"Found {len(page_markers)} page markers in the text")

            # If no page markers found, try the original pattern
            if not page_markers:
                page_markers = list(re.finditer(r'---\s*\{\s*}\s*---', content))
                print(f"Found {len(page_markers)} page markers using original pattern")

            # If still no page markers found, treat the entire file as one page
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

                    # Don't process the text yet - just store it as is
                    print(
                        f"Adding page {i + 1} with company name: '{company_name}' and content length: {len(page_content)}")
                    pages.append((page_content, company_name))

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

    def _process_hebrew_text(self, text, style=None, line_alignments=None, line_styles=None):
        """
        Process Hebrew text for proper display in the PDF.

        Args:
            text: Text to process
            style: Style to use for the text (defaults to self.hebrew_style)
            line_alignments: Optional list of alignment strings ('left', 'right', 'center') for each line
            line_styles: Optional list of style names ('normal', 'bold', 'italic', 'title', 'subtitle', 'quote') for each line

        Returns:
            Paragraph object or list of Paragraph objects with properly processed Hebrew text
        """
        if style is None:
            style = self.hebrew_style

        # Handle newlines by splitting the text and creating multiple paragraphs
        if '\n' in text:
            lines = text.split('\n')
            paragraphs = []

            for i, line in enumerate(lines):
                if not line.strip():  # Skip empty lines
                    paragraphs.append(Spacer(1, 0.1 * inch))
                    continue

                # Determine style for this line based on line_alignments and line_styles
                line_style = style

                # Apply style first
                if line_styles and i < len(line_styles):
                    style_name = line_styles[i].lower()
                    if style_name == 'bold':
                        line_style = self.bold_style
                    elif style_name == 'italic':
                        line_style = self.italic_style
                    elif style_name == 'title':
                        line_style = self.title_style
                    elif style_name == 'subtitle':
                        line_style = self.subtitle_style
                    elif style_name == 'quote':
                        line_style = self.quote_style

                # Then apply alignment if it should override the style's default
                if line_alignments and i < len(line_alignments):
                    alignment = line_alignments[i].lower()
                    # Create a copy of the style with the new alignment
                    if alignment == 'center':
                        new_style = ParagraphStyle(f'Custom_{i}', parent=line_style)
                        new_style.alignment = TA_CENTER
                        line_style = new_style
                    elif alignment == 'left':
                        new_style = ParagraphStyle(f'Custom_{i}', parent=line_style)
                        new_style.alignment = TA_LEFT
                        line_style = new_style
                    elif alignment == 'right':
                        new_style = ParagraphStyle(f'Custom_{i}', parent=line_style)
                        new_style.alignment = TA_RIGHT
                        line_style = new_style

                try:
                    reshaped_line = reshape(line)
                    bidi_line = bidialg(reshaped_line)
                    paragraphs.append(Paragraph(bidi_line, line_style))
                except Exception as e:
                    print(f"Error processing Hebrew text line: {e}, using unprocessed text")
                    paragraphs.append(Paragraph(line, line_style))

                # Add a small spacer between lines
                if i < len(lines) - 1:  # Don't add spacer after last line
                    paragraphs.append(Spacer(1, 0.1 * inch))

            return paragraphs
        else:
            # Process single-line text
            try:
                reshaped_content = reshape(text)
                bidi_content = bidialg(reshaped_content)
                return Paragraph(bidi_content, style)
            except Exception as e:
                print(f"Error processing Hebrew text: {e}, using unprocessed text")
                return Paragraph(text, style)

    def _add_section_divider(self, story, with_text=None):
        """Add a visual divider to the document with optional text"""
        story.append(Spacer(1, 0.25 * inch))

        if with_text:
            # Add a divider with text in the middle
            try:
                reshaped_text = reshape(with_text)
                bidi_text = bidialg(reshaped_text)
                divider_text = Paragraph(bidi_text, self.subtitle_style)
                story.append(divider_text)
            except Exception as e:
                print(f"Error processing divider text: {e}, using unprocessed text")
                divider_text = Paragraph(with_text, self.subtitle_style)
                story.append(divider_text)
        else:
            # Add a simple horizontal line
            story.append(HRFlowable(
                width="100%",
                thickness=1,
                color=colors.darkgrey,
                spaceBefore=0.1 * inch,
                spaceAfter=0.1 * inch
            ))

        story.append(Spacer(1, 0.15 * inch))

    def generate_pdf(self):
        """
        Generate the PDF with the specified header, footer, and content.
        """
        # Get page content
        pages_content = self._parse_text_file()

        if not pages_content:
            print("ERROR: No content pages to add to PDF")
            pages_content = [("No content was found to add to the PDF.", "Error")]

        # Create page template with header and footer
        frame = Frame(
            self.margin_left,
            self.margin_bottom,
            self.page_width - (self.margin_left + self.margin_right),
            self.page_height - (self.margin_top + self.margin_bottom),
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
                # Check if this page should have fixed text at the top
                if page_num in self.fixed_text and self.fixed_text[page_num].get("position") == "top":
                    fixed_text_content = self.fixed_text[page_num]["text"]

                    # Determine style based on alignment
                    fixed_text_style = self.fixed_text_style  # default
                    alignment = self.fixed_text[page_num].get("alignment", "right").lower()
                    if alignment == "center":
                        fixed_text_style = self.centered_text_style
                    elif alignment == "left":
                        fixed_text_style = self.left_text_style

                    # Get line-specific settings if specified
                    line_alignments = self.fixed_text[page_num].get("line_alignments")
                    line_styles = self.fixed_text[page_num].get("line_styles")

                    fixed_text_paras = self._process_hebrew_text(
                        fixed_text_content,
                        fixed_text_style,
                        line_alignments,
                        line_styles
                    )

                    # Handle both single paragraph and multiple paragraphs
                    if isinstance(fixed_text_paras, list):
                        story.extend(fixed_text_paras)
                    else:
                        story.append(fixed_text_paras)

                    story.append(Spacer(1, 0.25 * inch))  # Add space after fixed text

                # Add company name as a separate paragraph if exists
                if company_name.strip():
                    # Process company name for RTL display if it's in Hebrew
                    try:
                        reshaped_company = reshape(company_name)
                        bidi_company = bidialg(reshaped_company)
                        # Use the title style for company names
                        company_paragraph = Paragraph(bidi_company, self.title_style)
                    except Exception as e:
                        print(f"Error processing company name: {e}, using unprocessed text")
                        company_paragraph = Paragraph(company_name, self.title_style)

                    story.append(company_paragraph)
                    story.append(Spacer(1, 0.25 * inch))  # Add space after company name

                # Check if this page should have fixed text after company name
                if page_num in self.fixed_text and self.fixed_text[page_num].get("position") == "after_company":
                    fixed_text_content = self.fixed_text[page_num]["text"]

                    # Determine style based on alignment
                    fixed_text_style = self.fixed_text_style  # default
                    alignment = self.fixed_text[page_num].get("alignment", "right").lower()
                    if alignment == "center":
                        fixed_text_style = self.centered_text_style
                    elif alignment == "left":
                        fixed_text_style = self.left_text_style

                    # Get line-specific settings if specified
                    line_alignments = self.fixed_text[page_num].get("line_alignments")
                    line_styles = self.fixed_text[page_num].get("line_styles")

                    fixed_text_paras = self._process_hebrew_text(
                        fixed_text_content,
                        fixed_text_style,
                        line_alignments,
                        line_styles
                    )

                    # Handle both single paragraph and multiple paragraphs
                    if isinstance(fixed_text_paras, list):
                        story.extend(fixed_text_paras)
                    else:
                        story.append(fixed_text_paras)

                    # Add a section divider
                    self._add_section_divider(story)

                # Process main content
                hebrew_paragraphs = self._process_hebrew_text(page_content)

                # Handle both single paragraph and multiple paragraphs
                if isinstance(hebrew_paragraphs, list):
                    story.extend(hebrew_paragraphs)
                else:
                    story.append(hebrew_paragraphs)

                # Check if this page should have fixed text at the bottom
                if page_num in self.fixed_text and self.fixed_text[page_num].get("position") == "bottom":
                    # Add a section divider before the bottom text
                    self._add_section_divider(story)

                    fixed_text_content = self.fixed_text[page_num]["text"]

                    # Determine style based on alignment
                    fixed_text_style = self.fixed_text_style  # default
                    alignment = self.fixed_text[page_num].get("alignment", "right").lower()
                    if alignment == "center":
                        fixed_text_style = self.centered_text_style
                    elif alignment == "left":
                        fixed_text_style = self.left_text_style

                    # Get line-specific settings if specified
                    line_alignments = self.fixed_text[page_num].get("line_alignments")
                    line_styles = self.fixed_text[page_num].get("line_styles")

                    fixed_text_paras = self._process_hebrew_text(
                        fixed_text_content,
                        fixed_text_style,
                        line_alignments,
                        line_styles
                    )

                    # Handle both single paragraph and multiple paragraphs
                    if isinstance(fixed_text_paras, list):
                        story.extend(fixed_text_paras)
                    else:
                        story.append(fixed_text_paras)

                # Add page break after each page except the last one
                if page_num < len(pages_content):
                    story.append(PageBreak())

        # Build the PDF document
        try:
            self.doc.build(story)
            print("PDF generation completed successfully")
        except Exception as e:
            print(f"Error building PDF: {e}")


# Example usage with enhanced styling
if __name__ == "__main__":
    header_image_path = r"F:\projects\MBTInteligence\media\full_logo.png"
    footer_text = "created by Netta Ben Sinai"
    text_file_path = r"F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI-cleaned-hebrew.txt"
    output_path = r"F:\projects\MBTInteligence\output\nir-bensinai-MBTI-styled-hebrew.pdf"
    hebrew_font_path = r"F:\projects\MBTInteligence\media\fonts\FrankRuhlLibre-VariableFont_wght.ttf"

    # Define fixed text for specific pages with enhanced styling options
    fixed_text = {
        1: {  # Page 1
            "text": "פענוח דוח MBTI בתרגום לעברית\n"
                    f"{MBTI_name}\n"
                    f"{MBTI_date}\n"
                    f"הטיפוס שלך הוא:{MBTI_type}",
            "position": "top",
            "alignment": "center",
            "line_styles": ["title", "bold", "normal", "subtitle"]  # Apply different styles to each line
        },
        2: {  # Page 2
            "text": "הערה: מידע זה הוא לצרכי לימוד בלבד.\nאין להסתמך על מידע זה לצרכים מקצועיים.",
            "position": "bottom",
            "alignment": "right",
            "line_styles": ["bold", "italic"]  # First line bold, second italic
        },
        3: {  # Page 3
            "text": "תוכן מיוחד לעמוד 3\nשורה שנייה ממורכזת\nשורה שלישית",
            "position": "after_company",
            "line_alignments": ["right", "center", "right"],
            "line_styles": ["subtitle", "quote", "normal"]  # Different style for each line
        },
        4: {  # Page 4 - Mixed alignments and styles
            "text": "כותרת בעברית\nThis is English text aligned left\nטקסט עברי מיושר לימין",
            "position": "top",
            "line_alignments": ["center", "left", "right"],
            "line_styles": ["title", "normal", "bold"]
        }
    }

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

    # Create PDF generator with styling options
    pdf_gen = PDFGenerator(
        header_image_path=header_image_path,
        footer_text=footer_text,
        text_file_path=text_file_path,
        output_path=output_path,
        hebrew_font_path=hebrew_font_path,
        fixed_text=fixed_text,
        page_size=letter,  # You can use A4, landscape(letter), etc.
        background_color=colors.white,  # You can use any color from reportlab.lib.colors
        margins={'left': 0.75, 'right': 0.75, 'top': 1.0, 'bottom': 0.75},  # Custom margins in inches
        page_template='fancy'  # Use 'default', 'fancy', or 'watermark'
    )
    print("PDF generation started...")
    pdf_gen.generate_pdf()
    print(f"PDF generated at {output_path}")


# Example function to create a PDF with a table of MBTI types
def create_mbti_types_table(output_path):
    """Create a PDF with a table showing MBTI type information"""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add a title
    title_style = styles["Title"]
    title = Paragraph("MBTI Types Overview", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # MBTI types data
    data = [
        ['Type', 'Cognitive Functions', 'Typical Traits'],
        ['INTJ', 'Ni-Te-Fi-Se', 'Strategic, Independent, Analytical'],
        ['INTP', 'Ti-Ne-Si-Fe', 'Logical, Curious, Theoretical'],
        ['ENTJ', 'Te-Ni-Se-Fi', 'Decisive, Efficient, Strategic'],
        ['ENTP', 'Ne-Ti-Fe-Si', 'Innovative, Versatile, Argumentative'],
        ['INFJ', 'Ni-Fe-Ti-Se', 'Insightful, Principled, Complex'],
        ['INFP', 'Fi-Ne-Si-Te', 'Idealistic, Compassionate, Creative'],
        ['ENFJ', 'Fe-Ni-Se-Ti', 'Charismatic, Inspiring, Diplomatic'],
        ['ENFP', 'Ne-Fi-Te-Si', 'Enthusiastic, Creative, Sociable'],
        ['ISTJ', 'Si-Te-Fi-Ne', 'Reliable, Practical, Organized'],
        ['ISFJ', 'Si-Fe-Ti-Ne', 'Nurturing, Loyal, Traditional'],
        ['ESTJ', 'Te-Si-Ne-Fi', 'Efficient, Logical, Decisive'],
        ['ESFJ', 'Fe-Si-Ne-Ti', 'Supportive, Organized, Practical'],
        ['ISTP', 'Ti-Se-Ni-Fe', 'Adaptable, Observant, Practical'],
        ['ISFP', 'Fi-Se-Ni-Te', 'Gentle, Sensitive, Spontaneous'],
        ['ESTP', 'Se-Ti-Fe-Ni', 'Energetic, Adaptable, Pragmatic'],
        ['ESFP', 'Se-Fi-Te-Ni', 'Enthusiastic, Friendly, Spontaneous']
    ]

    # Create the table
    table = Table(data, colWidths=[50, 100, 200])

    # Style the table
    table_style = TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        # Data row styling (alternating rows)
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),
        ('BACKGROUND', (0, 4), (-1, 4), colors.lightgrey),
        ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
        ('BACKGROUND', (0, 8), (-1, 8), colors.lightgrey),
        ('BACKGROUND', (0, 10), (-1, 10), colors.lightgrey),
        ('BACKGROUND', (0, 12), (-1, 12), colors.lightgrey),
        ('BACKGROUND', (0, 14), (-1, 14), colors.lightgrey),
        ('BACKGROUND', (0, 16), (-1, 16), colors.lightgrey),

        # Grid styling
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),

        # Alignment for all cells
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Center type column
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Center functions column
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center all cells
    ])

    table.setStyle(table_style)
    elements.append(table)

    # Add explanatory text
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Cognitive Functions Key:", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    functions_text = """
    <b>Ni</b> - Introverted Intuition: Focus on internal abstract connections and conceptual patterns<br/>
    <b>Ne</b> - Extraverted Intuition: Exploring multiple possibilities and generating ideas<br/>
    <b>Si</b> - Introverted Sensing: Recalling detailed information and past experiences<br/>
    <b>Se</b> - Extraverted Sensing: Being aware of and responding to immediate experiences<br/>
    <b>Ti</b> - Introverted Thinking: Internal logical analysis and consistency<br/>
    <b>Te</b> - Extraverted Thinking: External organization and logical efficiency<br/>
    <b>Fi</b> - Introverted Feeling: Internal value alignment and authenticity<br/>
    <b>Fe</b> - Extraverted Feeling: Harmonizing with and responding to others' emotions
    """

    # Create a custom style for the functions explanation
    function_style = styles["Normal"]
    function_style.spaceAfter = 12

    elements.append(Paragraph(functions_text, function_style))

    # Build the PDF
    doc.build(elements)


# Example function to create MBTI profile with colorful visualization
def create_mbti_profile(person_name, mbti_type, output_path):
    """Create a personalized MBTI profile with visualizations"""
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Drawing
    from reportlab.graphics.shapes import Drawing, String, Rect
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    # Map of MBTI types to their cognitive functions and strengths
    type_data = {
        'INTJ': {
            'functions': ['Ni', 'Te', 'Fi', 'Se'],
            'strengths': [90, 80, 40, 30],
            'color': colors.darkblue,
            'description': "Strategic and independent, with a focus on systems and innovation. INTJs are driven to turn theories into clear plans and use logic and insight to achieve their goals."
        },
        'INTP': {
            'functions': ['Ti', 'Ne', 'Si', 'Fe'],
            'strengths': [90, 80, 40, 30],
            'color': colors.purple,
            'description': "Analytical and theoretical, with a focus on logical systems and original ideas. INTPs use their intellect to understand complex concepts and enjoy exploring possibilities."
        },
        'ENTJ': {
            'functions': ['Te', 'Ni', 'Se', 'Fi'],
            'strengths': [90, 80, 40, 30],
            'color': colors.darkgreen,
            'description': "Decisive and efficient, with a focus on organization and leadership. ENTJs are strategic thinkers who implement visions through practical planning and directing others."
        },
        # Add other types as needed
        'ISFP': {
            'functions': ['Fi', 'Se', 'Ni', 'Te'],
            'strengths': [90, 80, 40, 30],
            'color': colors.coral,
            'description': "Gentle and aesthetic, with a focus on personal values and sensory experiences. ISFPs are authentic individuals who appreciate beauty and prefer to live in the moment."
        },
    }

    # Default if type not found
    if mbti_type not in type_data:
        type_data[mbti_type] = {
            'functions': ['?', '?', '?', '?'],
            'strengths': [50, 50, 50, 50],
            'color': colors.grey,
            'description': f"Detailed information for {mbti_type} is not available in our database."
        }

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Create custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=24,
        textColor=type_data[mbti_type]['color']
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=type_data[mbti_type]['color']
    )

    # Add a title
    title = Paragraph(f"MBTI Profile: {person_name}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Add type information
    type_title = Paragraph(f"Type: {mbti_type}", subtitle_style)
    elements.append(type_title)
    elements.append(Spacer(1, 12))

    # Add type description
    elements.append(Paragraph(type_data[mbti_type]['description'], styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Add cognitive functions chart
    elements.append(Paragraph("Cognitive Functions", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    drawing = Drawing(400, 200)

    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = [type_data[mbti_type]['strengths']]
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 20
    bc.categoryAxis.labels.boxAnchor = 'n'
    bc.categoryAxis.labels.dx = 0
    bc.categoryAxis.labels.dy = -5
    bc.categoryAxis.categoryNames = type_data[mbti_type]['functions']
    bc.bars[0].fillColor = type_data[mbti_type]['color']

    drawing.add(bc)
    elements.append(drawing)
    elements.append(Spacer(1, 20))

    # Add explanation of functions
    elements.append(Paragraph("Understanding Your Cognitive Functions:", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    functions_text = f"""
    <b>Dominant Function ({type_data[mbti_type]['functions'][0]})</b>: This is your most developed and conscious cognitive process. It shapes much of your personality and is often used with confidence.<br/><br/>

    <b>Auxiliary Function ({type_data[mbti_type]['functions'][1]})</b>: This is your supporting process that balances your dominant function. It helps you communicate and interact with the world in a secondary way.<br/><br/>

    <b>Tertiary Function ({type_data[mbti_type]['functions'][2]})</b>: This function is less developed but becomes stronger with maturity. It often emerges in comfortable or supportive environments.<br/><br/>

    <b>Inferior Function ({type_data[mbti_type]['functions'][3]})</b>: This is your least developed function and can be a source of stress or growth. It often emerges under stress or when you're pushed outside your comfort zone.
    """

    elements.append(Paragraph(functions_text, styles["Normal"]))

    # Build the PDF
    doc.build(elements)