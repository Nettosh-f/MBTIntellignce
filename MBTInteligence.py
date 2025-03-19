import PyPDF2


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


# Example usage
if __name__ == "__main__":
    pdf_file_path = input(r"F:\projects\MBTInteligence\Adi-Chen-267149-30ffb71f-a3fd-ef11-90cb-000d3a58c2b2.pdf")
    output_file_path = input("./Output.txt")

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_file_path)

    # If an output path is provided, save the text to a file
    if output_file_path:
        # for i in range(text.count("\n--- Page") + 1):
        #     print(f"\n--- Page {i + 1} ---")
        save_text_to_file(text, output_file_path)

    else:
        # Otherwise print the text
        print("\nExtracted Text:")
        print(text)

