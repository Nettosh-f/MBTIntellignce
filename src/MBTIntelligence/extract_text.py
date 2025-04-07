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


def save_text_to_file(text, file_end, file_path):
    """
    Save extracted text to a text file.

    Args:
        text (str): Text to save
        file_end (str): Suffix to add to the output filename
        file_path (str): Path to the original PDF file
    """
    try:
        filename = os.path.splitext(os.path.basename(file_path))[0] + file_end
        output_path = os.path.join(r"F:\projects\MBTInteligence\output", filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")


def process_pdf_file(file_path: str, lines_to_remove_config: Dict[int, Union[str, List[int]]]) -> str:
    output_file_path = os.path.splitext(file_path)[0] + "-cleaned.txt"

    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for page_num in range(num_pages):
                    # Always write the page indicator
                    output_file.write(f"--- Page {page_num + 1} ---\n")

                    if page_num in lines_to_remove_config:
                        config = lines_to_remove_config[page_num]
                        if config == "ALL":
                            # Skip content but keep page indicator
                            output_file.write("\n")
                            continue
                        elif isinstance(config, list):
                            page = pdf_reader.pages[page_num]
                            text = page.extract_text().split('\n')
                            text = [line for i, line in enumerate(text) if i not in config]
                            output_file.write('\n'.join(text) + '\n\n')
                    else:
                        # If page is not in config, include all content
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        output_file.write(text + '\n\n')

        print(f"Processed PDF saved to: {output_file_path}")
        return output_file_path

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
