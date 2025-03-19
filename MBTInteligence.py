import PyPDF2
import os
import glob


def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text from the PDF
    """
    # Create a text string to store the extracted text
    extracted_text = ""

    try:
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Get the number of pages in the PDF
            num_pages = len(pdf_reader.pages)

            # Print the number of pages for information
            print(f"PDF has {num_pages} pages.")

            # Extract text from each page
            for page_num in range(num_pages):
                # Get the page object
                page = pdf_reader.pages[page_num]

                # Extract text from the page
                page_text = page.extract_text()

                # Add the page text to our string with a page separator
                extracted_text += f"\n--- Page {page_num + 1} ---\n"
                extracted_text += page_text

            print("Text extraction completed successfully.")

    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return extracted_text


def save_text_to_file(text, output_path):
    """
    Save extracted text to a text file.

    Args:
        text (str): Text to save
        output_path (str): Path where to save the text file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")


def process_pdf_file(pdf_path):
    """
    Process a single PDF file: extract text and save to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
    """
    print(f"\nProcessing: {pdf_path}")
    
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Generate output file path (same name but with .txt extension)
    output_path = os.path.splitext(pdf_path)[0] + ".txt"
    
    # Save the extracted text
    save_text_to_file(text, output_path)


def process_all_pdfs(directory="."):
    """
    Process all PDF files in the specified directory.
    
    Args:
        directory (str): Directory to search for PDF files (default: current directory)
    """
    # Find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {directory}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process.")
    
    # Process each PDF file
    for pdf_file in pdf_files:
        process_pdf_file(pdf_file)
    
    print("\nAll PDF files have been processed.")


# Example usage
if __name__ == "__main__":
    # Process all PDFs in the current directory
    process_all_pdfs()