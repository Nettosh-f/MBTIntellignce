import os
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.platypus import Paragraph, Frame, PageTemplate, BaseDocTemplate, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus.flowables import Spacer, Image, HRFlowable, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from bidi.algorithm import get_display as bidialg
from arabic_reshaper import reshape
from utils import find_type, get_date, get_name


class MBTIReportGenerator:
    def __init__(self, header_image_path, footer_text, text_file_path, output_path,
                 hebrew_font_path=None, fixed_text=None, mbti_data=None):
        """
        Initialize the PDF generator with necessary parameters.

        Args:
            header_image_path: Path to the PNG header image
            footer_text: Text to be used as footer
            text_file_path: Path to the text file with content
            output_path: Path where the PDF will be saved
            hebrew_font_path: Path to a Hebrew font file (TTF) for proper rendering
            fixed_text: Dictionary mapping page numbers to fixed text to insert
            mbti_data: Dictionary with MBTI results (type, name, date)
        """
        self.header_image_path = header_image_path
        self.footer_text = footer_text
        self.text_file_path = text_file_path
        self.output_path = output_path
        self.hebrew_font_path = hebrew_font_path
        self.fixed_text = fixed_text or {}

        # MBTI data (type, name, date)
        if mbti_data:
            self.mbti_type = mbti_data.get('type', '')
            self.mbti_name = mbti_data.get('name', '')
            self.mbti_date = mbti_data.get('date', '')
        else:
            # Get MBTI data from utils functions if not provided
            self.mbti_type = find_type(text_file_path)
            self.mbti_name = get_name(text_file_path)
            self.mbti_date = get_date(text_file_path)

        # Page setup
        self.page_size = letter
        self.page_width, self.page_height = self.page_size
        self.margins = {
            'left': 0.75 * inch,
            'right': 0.75 * inch,
            'top': 1.25 * inch,
            'bottom': 0.75 * inch
        }

        # Set up color scheme based on MBTI type before creating styles
        self.color_scheme = self._get_color_scheme(self.mbti_type)

        # Register Hebrew font
        self._register_fonts()

        # Initialize document
        self.doc = BaseDocTemplate(
            self.output_path,
            pagesize=self.page_size,
            leftMargin=self.margins['left'],
            rightMargin=self.margins['right'],
            topMargin=self.margins['top'],
            bottomMargin=self.margins['bottom']
        )

        # Create styles
        self.styles = getSampleStyleSheet()
        self._create_styles()

    def _register_fonts(self):
        """Register fonts needed for the document"""
        if self.hebrew_font_path and os.path.exists(self.hebrew_font_path):
            try:
                # Register the base Hebrew font
                pdfmetrics.registerFont(TTFont('Hebrew', self.hebrew_font_path))
                print(f"Successfully registered Hebrew font from {self.hebrew_font_path}")

                # Try to register bold/italic variants if they exist
                font_dir = os.path.dirname(self.hebrew_font_path)
                font_name = os.path.basename(self.hebrew_font_path)
                base_name = os.path.splitext(font_name)[0]

                # Common naming patterns for bold/italic variants
                bold_patterns = [f"{base_name}-Bold.ttf", f"{base_name}Bold.ttf", f"{base_name}_Bold.ttf"]
                italic_patterns = [f"{base_name}-Italic.ttf", f"{base_name}Italic.ttf", f"{base_name}_Italic.ttf"]

                # Try to register bold font
                for pattern in bold_patterns:
                    bold_path = os.path.join(font_dir, pattern)
                    if os.path.exists(bold_path):
                        pdfmetrics.registerFont(TTFont('Hebrew-Bold', bold_path))
                        print(f"Successfully registered Hebrew Bold font from {bold_path}")
                        break

                # Try to register italic font
                for pattern in italic_patterns:
                    italic_path = os.path.join(font_dir, pattern)
                    if os.path.exists(italic_path):
                        pdfmetrics.registerFont(TTFont('Hebrew-Italic', italic_path))
                        print(f"Successfully registered Hebrew Italic font from {italic_path}")
                        break
            except Exception as e:
                print(f"Warning: Could not register Hebrew font: {e}")
                print("Using default font instead. Hebrew text may not display correctly.")
        else:
            print(f"Warning: Hebrew font file not found at {self.hebrew_font_path}")
            print("Using default font instead. Hebrew text may not display correctly.")

    def _get_color_scheme(self, mbti_type):
        """Get color scheme based on MBTI type"""
        color_schemes = {
            'INTJ': {'primary': colors.navy, 'secondary': colors.darkblue, 'accent': colors.steelblue},
            'INTP': {'primary': colors.indigo, 'secondary': colors.purple, 'accent': colors.blueviolet},
            'ENTJ': {'primary': colors.darkblue, 'secondary': colors.blue, 'accent': colors.royalblue},
            'ENTP': {'primary': colors.blueviolet, 'secondary': colors.purple, 'accent': colors.mediumorchid},
            'INFJ': {'primary': colors.darkgreen, 'secondary': colors.forestgreen, 'accent': colors.seagreen},
            'INFP': {'primary': colors.darkturquoise, 'secondary': colors.teal, 'accent': colors.cadetblue},
            'ENFJ': {'primary': colors.darkmagenta, 'secondary': colors.mediumvioletred, 'accent': colors.hotpink},
            'ENFP': {'primary': colors.darkorange, 'secondary': colors.orange, 'accent': colors.coral},
            'ISTJ': {'primary': colors.saddlebrown, 'secondary': colors.sienna, 'accent': colors.peru},
            'ISFJ': {'primary': colors.darkslategray, 'secondary': colors.slategray, 'accent': colors.lightslategray},
            'ESTJ': {'primary': colors.maroon, 'secondary': colors.darkred, 'accent': colors.firebrick},
            'ESFJ': {'primary': colors.darkgoldenrod, 'secondary': colors.goldenrod, 'accent': colors.gold},
            'ISTP': {'primary': colors.dimgray, 'secondary': colors.gray, 'accent': colors.darkgray},
            'ISFP': {'primary': colors.lightseagreen, 'secondary': colors.mediumaquamarine,
                     'accent': colors.aquamarine},
            'ESTP': {'primary': colors.crimson, 'secondary': colors.red, 'accent': colors.tomato},
            'ESFP': {'primary': colors.deeppink, 'secondary': colors.hotpink, 'accent': colors.lightpink}
        }

        # Default color scheme if type not found
        default_scheme = {
            'primary': colors.darkblue,
            'secondary': colors.blue,
            'accent': colors.royalblue
        }

        return color_schemes.get(mbti_type, default_scheme)

    def _create_styles(self):
        """Create all the paragraph styles needed for the document"""
        # Base font settings
        hebrew_font = 'Hebrew' if hasattr(pdfmetrics, '_fonts') and 'Hebrew' in pdfmetrics._fonts else 'Helvetica'
        hebrew_bold = 'Hebrew-Bold' if hasattr(pdfmetrics,
                                               '_fonts') and 'Hebrew-Bold' in pdfmetrics._fonts else hebrew_font
        hebrew_italic = 'Hebrew-Italic' if hasattr(pdfmetrics,
                                                   '_fonts') and 'Hebrew-Italic' in pdfmetrics._fonts else hebrew_font

        # Footer style
        self.footer_style = ParagraphStyle(
            'FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            fontName=hebrew_font
        )

        # Main title (MBTI type) style
        self.mbti_title_style = ParagraphStyle(
            'MBTITitleStyle',
            parent=self.styles['Title'],
            alignment=TA_CENTER,
            fontName=hebrew_bold,
            fontSize=24,
            textColor=self.color_scheme['primary'],
            spaceAfter=12,
            spaceBefore=12,
            direction='rtl'
        )

        # Hebrew text (RTL) style
        self.hebrew_style = ParagraphStyle(
            'HebrewStyle',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT,
            fontName=hebrew_font,
            fontSize=10,
            leading=14,  # Line spacing
            direction='rtl'
        )

        # Fixed text styles
        self.fixed_text_style = ParagraphStyle(
            'FixedTextStyle',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT,
            fontName=hebrew_font,
            fontSize=10,
            direction='rtl',
        )

        # Centered text style
        self.centered_text_style = ParagraphStyle(
            'CenteredTextStyle',
            parent=self.styles['Normal'],
            alignment=TA_CENTER,
            fontName=hebrew_font,
            fontSize=10,
            direction='rtl',
        )

        # Left-aligned text style
        self.left_text_style = ParagraphStyle(
            'LeftTextStyle',
            parent=self.styles['Normal'],
            alignment=TA_LEFT,
            fontName=hebrew_font,
            fontSize=10,
        )

        # Section title style
        self.section_title_style = ParagraphStyle(
            'SectionTitleStyle',
            parent=self.styles['Heading1'],
            alignment=TA_RIGHT,
            fontName=hebrew_bold,
            fontSize=16,
            textColor=self.color_scheme['primary'],
            spaceBefore=12,
            spaceAfter=6,
            direction='rtl',
            borderWidth=0,
            borderColor=self.color_scheme['primary'],
            borderPadding=(0, 0, 2, 0),  # bottom padding only
            borderRadius=0
        )

        # Subsection title style
        self.subsection_title_style = ParagraphStyle(
            'SubsectionTitleStyle',
            parent=self.styles['Heading2'],
            alignment=TA_RIGHT,
            fontName=hebrew_bold,
            fontSize=14,
            textColor=self.color_scheme['secondary'],
            spaceBefore=8,
            spaceAfter=4,
            direction='rtl'
        )

        # Bold text style
        self.bold_style = ParagraphStyle(
            'BoldStyle',
            parent=self.hebrew_style,
            fontName=hebrew_bold,
            fontSize=10,
            direction='rtl',
        )

        # Italic text style
        self.italic_style = ParagraphStyle(
            'ItalicStyle',
            parent=self.hebrew_style,
            fontName=hebrew_italic,
            fontSize=10,
            direction='rtl',
            textColor=colors.darkslategray
        )

        # Quote box style
        self.quote_style = ParagraphStyle(
            'QuoteStyle',
            parent=self.hebrew_style,
            leftIndent=20,
            rightIndent=20,
            fontName=hebrew_italic,
            fontSize=10,
            textColor=colors.darkslategray,
            direction='rtl',
            borderWidth=1,
            borderColor=self.color_scheme['accent'],
            borderPadding=5,
            borderRadius=5,
            backColor=colors.white
        )

        # Highlight box style for important information
        self.highlight_style = ParagraphStyle(
            'HighlightStyle',
            parent=self.hebrew_style,
            fontName=hebrew_bold,
            fontSize=11,
            alignment=TA_CENTER,
            backColor=self.color_scheme['accent'].clone(alpha=0.15),
            borderColor=self.color_scheme['accent'],
            borderWidth=1,
            borderPadding=6,
            borderRadius=4,
            spaceBefore=6,
            spaceAfter=6
        )

        # English text style (for bilingual content)
        self.english_style = ParagraphStyle(
            'EnglishStyle',
            parent=self.styles['Normal'],
            alignment=TA_LEFT,
            fontName='Helvetica',
            fontSize=10,
        )

        # Person name style (for name display)
        self.name_style = ParagraphStyle(
            'NameStyle',
            parent=self.styles['Title'],
            alignment=TA_CENTER,
            fontName=hebrew_bold,
            fontSize=20,
            textColor=self.color_scheme['primary'],
            spaceBefore=0,
            spaceAfter=6,
            direction='rtl'
        )

        # Date style (for date display)
        self.date_style = ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            alignment=TA_CENTER,
            fontName=hebrew_font,
            fontSize=12,
            spaceBefore=0,
            spaceAfter=18,
            direction='rtl'
        )

    def _header_footer(self, canvas, doc):
        """
        Add the header and footer to each page.
        """
        # Save canvas state
        canvas.saveState()

        # Draw a colored bar at the top
        canvas.setFillColor(self.color_scheme['primary'])
        canvas.rect(0, self.page_height - 0.5 * inch, self.page_width, 0.5 * inch, fill=1, stroke=0)

        # Draw a thin colored line at bottom
        canvas.setStrokeColor(self.color_scheme['primary'])
        canvas.setLineWidth(2)
        canvas.line(0, 0.75 * inch, self.page_width, 0.75 * inch)

        # Add header (PNG image)
        if os.path.exists(self.header_image_path):
            try:
                # Position the image centered and below the colored bar
                img = Image(self.header_image_path, width=self.page_width * 0.8, height=0.5 * inch)
                img_width, img_height = img.wrap(0, 0)  # Get image dimensions
                img.drawOn(canvas, (self.page_width - img_width) / 2,
                           self.page_height - 0.75 * inch)
            except Exception as e:
                print(f"Error with header image: {e}")
                # Fallback: just write a text header
                canvas.setFont('Helvetica-Bold', 14)
                canvas.setFillColor(colors.black)
                canvas.drawString(self.margins['left'], self.page_height - 0.75 * inch, "MBTI REPORT")
        else:
            print(f"Header image not found at: {self.header_image_path}")
            canvas.setFont('Helvetica-Bold', 14)
            canvas.setFillColor(colors.black)
            canvas.drawString(self.margins['left'], self.page_height - 0.75 * inch, "MBTI REPORT")

        # Add footer text
        footer = Paragraph(f"{self.footer_text} - Page {doc.page}", self.footer_style)
        footer.wrapOn(canvas, self.page_width - 2 * self.margins['left'], 0.25 * inch)
        footer.drawOn(canvas, self.margins['left'], 0.5 * inch)

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
                    # Try to extract section title (assuming it's the first line)
                    lines = page_content.split('\n')
                    section_title = ""

                    if lines and lines[0].strip() and not lines[0].startswith("---"):
                        # Assume first non-empty line that's not a marker is a section title
                        section_title = lines[0].strip()
                        # Remove section title from content to process rest as Hebrew
                        page_content = '\n'.join(lines[1:]).strip()

                    print(
                        f"Adding page {i + 1} with section: '{section_title}' and content length: {len(page_content)}")
                    pages.append((page_content, section_title))

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
            line_styles: Optional list of style names ('normal', 'bold', 'italic', 'title', etc.) for each line

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
                        line_style = self.section_title_style
                    elif style_name == 'subtitle':
                        line_style = self.subsection_title_style
                    elif style_name == 'quote':
                        line_style = self.quote_style
                    elif style_name == 'highlight':
                        line_style = self.highlight_style

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
                    # For English text (doesn't need reshaping/bidirectional)
                    if all(ord(char) < 128 for char in line.strip()):
                        if line_style.alignment == TA_LEFT:
                            paragraphs.append(Paragraph(line, self.english_style))
                        else:
                            paragraphs.append(Paragraph(line, line_style))
                    else:
                        # Process Hebrew text
                        reshaped_line = reshape(line)
                        bidi_line = bidialg(reshaped_line)
                        paragraphs.append(Paragraph(bidi_line, line_style))
                except Exception as e:
                    print(f"Error processing text line: {e}, using unprocessed text")
                    paragraphs.append(Paragraph(line, line_style))

                # Add a small spacer between lines
                if i < len(lines) - 1:  # Don't add spacer after last line
                    paragraphs.append(Spacer(1, 0.1 * inch))

            return paragraphs
        else:
            # Process single-line text
            try:
                # For English text (doesn't need reshaping/bidirectional)
                if all(ord(char) < 128 for char in text.strip()):
                    if style.alignment == TA_LEFT:
                        return Paragraph(text, self.english_style)
                    else:
                        return Paragraph(text, style)
                else:
                    # Process Hebrew text
                    reshaped_content = reshape(text)
                    bidi_content = bidialg(reshaped_content)
                    return Paragraph(bidi_content, style)
            except Exception as e:
                print(f"Error processing text: {e}, using unprocessed text")
                return Paragraph(text, style)

    def _add_section_divider(self, story, with_text=None):
        """Add a visual divider to the document with optional text"""
        story.append(Spacer(1, 0.25 * inch))

        if with_text:
            # Add a divider with text in the middle
            try:
                reshaped_text = reshape(with_text)
                bidi_text = bidialg(reshaped_text)
                divider_text = Paragraph(bidi_text, self.section_title_style)
                story.append(divider_text)
            except Exception as e:
                print(f"Error processing divider text: {e}, using unprocessed text")
                divider_text = Paragraph(with_text, self.section_title_style)
                story.append(divider_text)

            # Add a thin line under the section title
            story.append(HRFlowable(
                width="100%",
                thickness=1,
                color=self.color_scheme['primary'],
                spaceBefore=0,
                spaceAfter=0.2 * inch
            ))
        else:
            # Add a simple horizontal line
            story.append(HRFlowable(
                width="100%",
                thickness=1,
                color=self.color_scheme['accent'],
                spaceBefore=0.1 * inch,
                spaceAfter=0.1 * inch
            ))

        story.append(Spacer(1, 0.15 * inch))

    def _create_mbti_title_page(self, story):
        """Create a beautiful title page for the MBTI report"""
        # Add title
        title_text = "פענוח דוח MBTI בתרגום לעברית"
        title = self._process_hebrew_text(title_text, self.mbti_title_style)
        story.append(title)
        story.append(Spacer(1, 0.5 * inch))

        # Add person's name
        if self.mbti_name:
            name = self._process_hebrew_text(self.mbti_name, self.name_style)
            story.append(name)

        # Add date
        if self.mbti_date:
            date = self._process_hebrew_text(self.mbti_date, self.date_style)
            story.append(date)

        # Add interpreter name ("פורש על ידי")
        interpreter_text = "פורש על ידי"
        interpreter = self._process_hebrew_text(interpreter_text, self.hebrew_style)
        story.append(interpreter)
        story.append(Spacer(1, 0.25 * inch))

        # Add MBTI type in large, colored text
        if self.mbti_type:
            type_text = f"הטיפוס שלך הוא: {self.mbti_type}"
            mbti_type = self._process_hebrew_text(type_text, self.mbti_title_style)
            story.append(mbti_type)

        # Add decorative element
        story.append(Spacer(1, 0.5 * inch))
        story.append(HRFlowable(
            width="50%",
            thickness=2,
            color=self.color_scheme['accent'],
            hAlign='CENTER'
        ))

        # Add interpreter credits at bottom if available
        story.append(Spacer(1, 1 * inch))
        credits_text = "חגית גיורא\nהמרכז הישראלי ל-MBTI"
        credits = self._process_hebrew_text(credits_text, self.centered_text_style)
        if isinstance(credits, list):
            story.extend(credits)
        else:
            story.append(credits)

        # Add page break after title page
        story.append(PageBreak())

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
            self.margins['left'],
            self.margins['bottom'],
            self.page_width - (self.margins['left'] + self.margins['right']),
            self.page_height - (self.margins['top'] + self.margins['bottom']),
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

        # Create title page
        self._create_mbti_title_page(story)

        print(f"Building PDF with {len(pages_content)} pages")

        for page_num, (page_content, section_title) in enumerate(pages_content, 1):
            print(f"Processing page {page_num}: Section: '{section_title}', Content length: {len(page_content)}")

            if page_content.strip() or section_title.strip():  # Skip empty pages
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

                # Add section title as a major heading if exists
                if section_title.strip():
                    # Process section title for RTL display
                    section_heading = self._process_hebrew_text(section_title, self.section_title_style)
                    story.append(section_heading)

                    # Add a decorative line under the section title
                    story.append(HRFlowable(
                        width="100%",
                        thickness=1,
                        color=self.color_scheme['primary'],
                        spaceBefore=0,
                        spaceAfter=0.2 * inch
                    ))

                    story.append(Spacer(1, 0.15 * inch))  # Add space after section title

                # Check if this page should have fixed text after section title
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

                    # For section 3, add a fancy box around the content
                    if page_num == 3:
                        # Create a decorated box for content
                        box_content = []
                        if isinstance(fixed_text_paras, list):
                            box_content.extend(fixed_text_paras)
                        else:
                            box_content.append(fixed_text_paras)

                        # Add the content to the story with styling
                        for para in box_content:
                            if not isinstance(para, Spacer):
                                # Create style for box content with background color
                                box_style = ParagraphStyle(
                                    'BoxStyle',
                                    parent=para.style,
                                    borderWidth=1,
                                    borderColor=self.color_scheme['accent'],
                                    borderPadding=5,
                                    borderRadius=5,
                                    backColor=colors.lavender
                                )
                                # Apply the box style to the paragraph
                                try:
                                    story.append(Paragraph(para.text, box_style))
                                except:
                                    # Fallback if para.text is not accessible
                                    story.append(para)
                            else:
                                story.append(para)
                    else:
                        # Handle both single paragraph and multiple paragraphs
                        if isinstance(fixed_text_paras, list):
                            story.extend(fixed_text_paras)
                        else:
                            story.append(fixed_text_paras)

                    story.append(Spacer(1, 0.3 * inch))  # Add space after fixed text

                # Process main content
                # Try to identify subsections in the content
                if page_content.strip():
                    content_parts = self._parse_sections(page_content)

                    for part in content_parts:
                        if isinstance(part, tuple):
                            # This is a heading with content
                            heading, content = part

                            # Add heading
                            heading_para = self._process_hebrew_text(heading, self.subsection_title_style)
                            story.append(heading_para)

                            # Add content
                            content_paras = self._process_hebrew_text(content, self.hebrew_style)
                            if isinstance(content_paras, list):
                                story.extend(content_paras)
                            else:
                                story.append(content_paras)

                            story.append(Spacer(1, 0.15 * inch))
                        else:
                            # This is just regular content without a heading
                            content_paras = self._process_hebrew_text(part, self.hebrew_style)
                            if isinstance(content_paras, list):
                                story.extend(content_paras)
                            else:
                                story.append(content_paras)

                # Check if this page should have fixed text at the bottom
                if page_num in self.fixed_text and self.fixed_text[page_num].get("position") == "bottom":
                    # Add a divider before the bottom text
                    story.append(Spacer(1, 0.25 * inch))
                    story.append(HRFlowable(
                        width="100%",
                        thickness=1,
                        color=self.color_scheme['accent'],
                        spaceBefore=0.1 * inch,
                        spaceAfter=0.1 * inch
                    ))

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

                    # For page 2, style the disclaimer in a highlight box
                    if page_num == 2:
                        disclaimer_style = self.highlight_style
                        disclaimer_paras = self._process_hebrew_text(
                            fixed_text_content,
                            disclaimer_style
                        )
                    else:
                        disclaimer_paras = self._process_hebrew_text(
                            fixed_text_content,
                            fixed_text_style,
                            line_alignments,
                            line_styles
                        )

                    # Handle both single paragraph and multiple paragraphs
                    if isinstance(disclaimer_paras, list):
                        story.extend(disclaimer_paras)
                    else:
                        story.append(disclaimer_paras)

                # Add page break after each page except the last one
                if page_num < len(pages_content):
                    story.append(PageBreak())

        # Build the PDF document
        try:
            self.doc.build(story)
            print("PDF generation completed successfully")
            return True
        except Exception as e:
            print(f"Error building PDF: {e}")
            return False

    def _parse_sections(self, content):
        """Parse content into sections based on formatting patterns"""
        # Split content by lines
        lines = content.split('\n')

        # Initialize result and current section
        sections = []
        current_heading = None
        current_content = []

        for line in lines:
            stripped_line = line.strip()

            if not stripped_line:
                # Empty line - add to current content
                current_content.append('')
                continue

            # Check if this line looks like a heading
            is_heading = False

            # Heading patterns:
            # 1. Short line followed by a line break
            # 2. Line ending with colon
            # 3. Line that has special punctuation at the beginning
            if (len(stripped_line) < 40 and (
                    stripped_line.endswith(':') or
                    stripped_line.startswith('•') or
                    stripped_line.startswith('-') or
                    any(marker in stripped_line for marker in ['––', '--', '—'])
            )):
                is_heading = True

            if is_heading:
                # If we already have a heading and content, add them to sections
                if current_heading is not None and current_content:
                    sections.append((current_heading, '\n'.join(current_content)))
                    current_content = []

                current_heading = stripped_line

            else:
                # Regular content - add to current content
                if current_content or current_heading is not None:
                    current_content.append(line)
                else:
                    # This is content without a heading
                    sections.append(line)

        # Add the last section if there is any
        if current_heading is not None and current_content:
            sections.append((current_heading, '\n'.join(current_content)))
        elif current_content:
            # If we have content without a heading at the end
            sections.append('\n'.join(current_content))

        return sections


# Example usage with styling options
if __name__ == "__main__":
    header_image_path = r"F:\projects\MBTInteligence\media\full_logo.png"
    footer_text = "created by Netta Ben Sinai"
    text_file_path = r"F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI-cleaned-hebrew.txt"
    output_path = r"F:\projects\MBTInteligence\output\nir-bensinai-MBTI-styled-hebrew.pdf"
    hebrew_font_path = r"F:\projects\MBTInteligence\media\fonts\FrankRuhlLibre-VariableFont_wght.ttf"

    # Get MBTI data
    mbti_type = find_type(text_file_path)
    mbti_name = get_name(text_file_path)
    mbti_date = get_date(text_file_path)

    # Create MBTI data dictionary
    mbti_data = {
        'type': mbti_type,
        'name': mbti_name,
        'date': mbti_date
    }

    # Define fixed text for specific pages with enhanced styling options
    fixed_text = {
        1: {  # Page 1 (already handled by the title page)
            "text": "",
            "position": "top"
        },
        2: {  # Page 2 - Disclaimer at bottom
            "text": "הערה: מידע זה הוא לצרכי לימוד בלבד.\nאין להסתמך על מידע זה לצרכים מקצועיים.",
            "position": "bottom",
            "alignment": "right"
        },
        3: {  # Page 3 - Special content after section title in a styled box
            "text": "תוכן מיוחד לעמוד 3\nשורה שנייה ממורכזת\nשורה שלישית",
            "position": "after_company",
            "line_alignments": ["right", "center", "right"],
            "line_styles": ["subtitle", "italic", "normal"]
        },
        4: {  # Page 4 - Mixed alignments and styles
            "text": "כותרת בעברית\nThis is English text aligned left\nטקסט עברי מיושר לימין",
            "position": "top",
            "line_alignments": ["center", "left", "right"],
            "line_styles": ["subtitle", "normal", "bold"]
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

    # Create PDF generator and generate PDF
    pdf_gen = MBTIReportGenerator(
        header_image_path=header_image_path,
        footer_text=footer_text,
        text_file_path=text_file_path,
        output_path=output_path,
        hebrew_font_path=hebrew_font_path,
        fixed_text=fixed_text,
        mbti_data=mbti_data
    )

    print("PDF generation started...")
    result = pdf_gen.generate_pdf()

    if result:
        print(f"PDF generated successfully at {output_path}")
    else:
        print("PDF generation failed. See error messages above.")