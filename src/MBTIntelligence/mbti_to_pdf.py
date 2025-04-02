import os
import pathlib
import webbrowser
from weasyprint import HTML


def generate_mbti_report(input_file, output_html, output_pdf, logo_path):
    # File paths
    header_image_url = pathlib.Path(logo_path).absolute().as_uri()

    # Read and split text
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    pages = [p.strip() for p in text.split('--- Page ') if p.strip() and not p.strip().isdigit()]
    total_pages = len(pages)

    # Footer static text
    footer_static_text = '© 2025 המרכז הישראלי ל-MBTI. כל הזכויות שמורות.'

    # Build HTML
    html_content = generate_html_content(header_image_url, pages, total_pages, footer_static_text)

    # Save HTML
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Generate PDF
    HTML(output_html).write_pdf(output_pdf)

    # Open HTML and PDF
    webbrowser.open(f'file://{os.path.abspath(output_html)}')
    webbrowser.open(f'file://{os.path.abspath(output_pdf)}')

    print("✅ MBTI report generated with page titles and numbers.")


def generate_html_content(header_image_url, pages, total_pages, footer_static_text):
    html_head = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 120px 60px 80px 60px;
            }}
            body {{
                font-family: 'Arial', sans-serif;
                direction: rtl;
                font-size: 16px;
                line-height: 1.8;
                color: #000;
            }}
            header {{
                position: fixed;
                top: -100px;
                left: 0;
                right: 0;
                text-align: center;
            }}
            header img {{
                height: 70px;
            }}
            footer {{
                position: fixed;
                bottom: -60px;
                left: 0;
                right: 0;
                font-size: 12px;
                color: gray;
                display: flex;
                justify-content: space-between;
                padding: 0 30px;
            }}
            .page {{
                page-break-after: always;
            }}
            main {{
                white-space: pre-wrap;
            }}
            .page-title {{
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 30px;
                color: #333;
            }}
        </style>
    </head>
    <body>
    """

    html_body = ""
    for index, page in enumerate(pages):
        page_number_text = f"עמוד {index + 1} מתוך {total_pages}"
        page_html = page.replace('\n', '<br>')

        html_body += f"""
        <div class="page">
            <header><img src="{header_image_url}" alt="Header Image"></header>
            <footer>
                <div>{page_number_text}</div>
                <div>{footer_static_text}</div>
            </footer>
            <main>
                <div class="page-title">{page_number_text}</div>
                {page_html}
            </main>
        </div>
        """

    html_footer = "</body></html>"

    return html_head + html_body + html_footer


if __name__ == "__main__":
    input_file = r'F:\projects\MBTInteligence\MBTItranslated\asaf-solomon-MBTI-fixed.txt'
    output_html = r'F:\projects\MBTInteligence\html files\mbti_report.html'
    output_pdf = r'F:\projects\MBTInteligence\MBTIpdfs\mbti_report.pdf'
    logo_path = r"F:\projects\Temp\full_logo.png"

    generate_mbti_report(input_file, output_html, output_pdf, logo_path)
