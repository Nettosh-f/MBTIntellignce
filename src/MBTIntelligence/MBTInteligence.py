import PyPDF2
import os
import glob
from dotenv import load_dotenv
import google.generativeai as genai
import time
import re

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)


def extract_text_from_pdf(pdf_path):
    extracted_text = ""

    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"PDF has {num_pages} pages.")

            for page_num in range(num_pages):

                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                # pattern = r'^(?:[^\n]*\n){4}(.*\n)(.*\n)(.*)$'
                # page_text = re.sub(pattern, r'\1\3', page_text, flags=re.MULTILINE)
                # print(f"Text extracted from page {page_num + 1}:\n" + pattern)
                if page_num == 0:
                    remove_list = ["Developed by\n", "Naomi L. Quenk, PhD  \n", "Jean M. Kummerow, PhD\n",
                                   "Myers-Briggs Type Indicator® Step II™ Interpretive Report  Copyright  2001,",
                                   " 2003, 2015 by Peter B. Myers and Katharine D. Myers. All rights \n",
                                   "reserved. Myers-Briggs Type Indicator, Myers-Briggs, MBTI, Step I, Step II, ",
                                   "the MBTI logo, and The Myers-Briggs Company logo are trade -\n",
                                   "marks or registered trademarks of The Myers & Briggs Foundation",
                                   " in the United States and other countries.+1 800 624 1765",
                                   "  |  www.themyersbriggs.comPrepared for\n"]
                    for i in range(0, 10):
                        cut_off_content = remove_list[i]
                        page_text = page_text.replace(cut_off_content, "")
                        print(f"successfully extracted text from page {page_num + 1}.")
                        print(f"Text after removing {cut_off_content}:\n")
                        print(page_text)
                    pattern = r'^(?:[^\n]*\n){1}(.*\n)(.*\n)(.*)$'
                    page_text = re.sub(pattern, r'\1\3', page_text, flags=re.MULTILINE)
                    print(f"Text extracted from page {page_num + 1}:\n" + pattern)
                elif page_num == 1:
                    # Remove content from page 2
                    page_text = ""
                    print(f"successfully extracted text from page {page_num + 1}.")
                    print(page_text)
                # elif page_num == 2:
                # elif page_num == 3:
                # elif page_num == 4:

                extracted_text += f"\n--- Page {page_num + 1} ---\n\n"
                extracted_text += page_text

            print("Text extraction completed successfully.")

    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return extracted_text


def clean_text_with_generative_ai(text):
    start_time = time.time()
    cleaned_text = ""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Please clean the following text: {text}, remove all footers and headers, but keep the page count."
    response = model.generate_content(prompt, generation_config={"temperature": 0.0})
    response_time = time.time() - start_time
    cleaned_text = response.text.strip()
    print(response.usage_metadata)
    print(f"Response time: {response_time * 1000:.4f} miliseconds")
    # print("response successful", response.text)
    return cleaned_text


def save_text_to_file(text, file_end, file_path):
    """
    Save extracted text to a text file.

    Args:
        text (str): Text to save
        output_path (str): Path where to save the text file
    """
    try:
        filename = os.path.splitext(os.path.basename(file_path))[0] + file_end
        output_path = os.path.join("./MBTItxt", filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")


def process_pdf_file(pdf_path):
    """
    Process a single PDF file: extract text, clean it, and save to a text file.

    Args:
        pdf_path (str): Path to the PDF file
    """
    print(f"\nProcessing: {pdf_path}")

    text = extract_text_from_pdf(pdf_path)
    save_text_to_file(text, "_raw.txt", pdf_path)

    # Clean the extracted text using Generative AI
    # cleaned_text = clean_text_with_generative_ai(text)
    # # print(cleaned_text)
    # save_text_to_file(text, "_cleaned.txt", pdf_path)


if __name__ == "__main__":
    process_pdf_file("MBTIpdfs/nir-bensinai-MBTI.pdf")