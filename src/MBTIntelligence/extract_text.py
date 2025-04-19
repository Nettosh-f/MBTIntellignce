import PyPDF2
import os
import glob
from dotenv import load_dotenv
import time
import re
from typing import Dict, Union, List


def extract_text_from_pdf(pdf_path, lines_to_remove_by_page):
    extracted_text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"PDF has {num_pages} pages.")

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()

                # Split the text into lines
                lines = page_text.split('\n')

                # Process page text based on lines_to_remove_by_page
                if lines_to_remove_by_page and page_num in lines_to_remove_by_page:
                    if lines_to_remove_by_page[page_num] == "ALL":
                        lines = []
                        print(f"Skipped all content from page {page_num + 1}.")
                    else:
                        remove_items = lines_to_remove_by_page[page_num]
                        if all(isinstance(item, int) for item in remove_items):
                            lines = [line for i, line in enumerate(lines) if i not in remove_items]
                        else:
                            lines = [line for line in lines if not any(item in line for item in remove_items)]

                # Join the processed lines
                processed_page_text = '\n'.join(lines)
                print(f"Processed page number {page_num+1} {processed_page_text}:")
                # Add page delimiter
                extracted_text += f"\n--- Page {page_num + 1} ---\n\n"
                extracted_text += processed_page_text + "\n"

            print("Text extraction completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return extracted_text


def process_pdf_file(file_path: str, lines_to_remove_config: Dict[int, Union[str, List[int]]]) -> str:
    # Get the project root directory (assuming the script is in src/MBTIntelligence/)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Create the output directory in the project root
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    raw_output_path = os.path.join(output_dir, f"{base_name}_raw.txt")
    cleaned_output_path = os.path.join(output_dir, f"{base_name}_cleaned.txt")

    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            # First, save the raw extracted text
            with open(raw_output_path, 'w', encoding='utf-8') as raw_file:
                for page_num in range(num_pages):
                    raw_file.write(f"--- Page {page_num + 1} ---\n")
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    raw_file.write(text + '\n\n')

            print(f"Raw extracted text saved to: {raw_output_path}")

            # Now process and save the cleaned text
            with open(cleaned_output_path, 'w', encoding='utf-8') as cleaned_file:
                for page_num in range(num_pages):
                    cleaned_file.write(f"--- Page {page_num + 1} ---\n")

                    if page_num in lines_to_remove_config:
                        config = lines_to_remove_config[page_num]
                        if config == "ALL":
                            cleaned_file.write("\n")
                            continue
                        elif isinstance(config, list):
                            page = pdf_reader.pages[page_num]
                            text = page.extract_text().split('\n')
                            text = [line for i, line in enumerate(text) if i not in config]
                            cleaned_file.write('\n'.join(text) + '\n\n')
                    else:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        cleaned_file.write(text + '\n\n')

        print(f"Cleaned text saved to: {cleaned_output_path}")
        return cleaned_output_path

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {str(e)}")
        return None


if __name__ == "__main__":
    # Process a single file with custom line removal configuration
    process_pdf_file(
        r"F:\projects\MBTInteligence\MBTIpdfs\asaf-solomon-267149-4ae2ac9c-005e-ef11-bdfd-6045bd04b01a.pdf",
        lines_to_remove_config={
            0: [0, 1, 2, 3, 4, 5, 6, 7],
            1: "ALL",  # Skip entire page
            2: [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
                38, 39, 40],
            3: "ALL",
            4: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
            5: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
            6: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
            7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
            8: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
            9: [0, 1, 2, 3, 4, 5, 6, 7, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
            10: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            11: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            12: [0, 1, 2, 4, 5, 6, 7, 8, 27, 28, 29, 30, 31],
            13: [0, 1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            14: "ALL",
            15: [0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
            16: [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                 61, 62, 63, 64, 65, 66]
        }
    )

    # Alternatively, process all PDFs in a directory with default configuration
    """
    pdf_dir = r"F:\projects\MBTInteligence\MBTIpdfs"
    for pdf_file in glob.glob(os.path.join(pdf_dir, "*.pdf")):
        process_pdf_file(pdf_file)
    """
