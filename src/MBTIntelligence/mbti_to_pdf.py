import os
import re
import pathlib
import webbrowser
from weasyprint import HTML
from datetime import datetime


def generate_mbti_report(input_file, output_html, output_pdf, logo_path, first_title):
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
    html_content = generate_html_content(header_image_url, pages, total_pages, footer_static_text, first_title)

    # Save HTML
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Generate PDF
    HTML(output_html).write_pdf(output_pdf)

    # Open HTML and PDF
    webbrowser.open(f'file://{os.path.abspath(output_html)}')
    webbrowser.open(f'file://{os.path.abspath(output_pdf)}')

    print("✅ MBTI report generated with page titles and numbers.")


def apply_formatting(text):
    # Bold and underline formatting
    text = re.sub(r'__\*\*(.*?)\*\*__', r'<b><u>\1</u></b>', text)

    # Bold formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Underline formatting
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)

    # Replace newlines with <br> tags
    text = text.replace('\n', '<br>')

    return text


def generate_html_content(header_image_url, pages, total_pages, footer_static_text, first_page_title):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
            .first-page {{
                text-align: center;
            }}
            .first-page-title {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 50px;
                color: #333;
                text-decoration: underline;
                padding-bottom: 10px;
            }}
            .timestamp {{
                font-size: 10px;
                color: #999;
            }}
            .bold {{
                font-weight: bold;
            }}
            .underline {{
                text-decoration: underline;
        </style>
    </head>
    <body>
    """

    html_body = ""
    for index, page in enumerate(pages):
        page_number_text = f"עמוד {index + 1} מתוך {total_pages}"
        page_content = re.sub(r'^\d+\s+---\s*', '', page).replace('\n', '<br>')
        page_content = apply_formatting(page_content)

        if index == 0:
            html_body += f"""
            <div class="page first-page">
                <header><img src="{header_image_url}" alt="Header Image"></header>
                <footer>
                    <div>{page_number_text}</div>
                    <div>{footer_static_text}</div>
                    <div class="timestamp"> created at: {current_time}</div>
                </footer>
                <main>
                    <div class="first-page-title">{first_page_title}</div>
                    <p>{page_content}</p>
                </main>
            </div>
            """
        else:
            html_body += f"""
            <div class="page">
                <header><img src="{header_image_url}" alt="Header Image"></header>
                <footer>
                    <div>{page_number_text}</div>
                    <div>{footer_static_text}</div>
                    <div class="timestamp"> created at: {current_time}</div>
                </footer>
                <main>
                    <div class="page-title">{page_number_text}</div>
                    <p>{page_content}</p>
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
    first_page_title = "דו״ח בתרגום לעברית עבור: "

    generate_mbti_report(input_file, output_html, output_pdf, logo_path, first_page_title)

