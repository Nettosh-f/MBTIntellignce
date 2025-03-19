import PyPDF2
import tkinter as tk
from tkinter import scrolledtext, filedialog


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


def visualize_text(text, pdf_path):
    """
    Display the extracted text in a GUI window.
    
    Args:
        text (str): The extracted text to display
        pdf_path (str): Path to the PDF file (for window title)
    """
    # Create the main window
    root = tk.Tk()
    root.title(f"PDF Text Viewer - {pdf_path}")
    root.geometry("800x600")
    
    # Create a frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.X, padx=5, pady=5)
    
    # Create a save button
    def save_text():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            save_text_to_file(text, file_path)
    
    save_button = tk.Button(button_frame, text="Save Text", command=save_text)
    save_button.pack(side=tk.LEFT, padx=5)
    
    # Create a scrolled text widget to display the text
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 10))
    text_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
    
    # Insert the text into the text area
    text_area.insert(tk.INSERT, text)
    
    # Make the text read-only
    text_area.config(state=tk.DISABLED)
    
    # Start the GUI event loop
    root.mainloop()


# Example usage
if __name__ == "__main__":
    pdf_file_path = input("Enter PDF file path (or press Enter for file dialog): ")
    
    # If no path is provided, open a file dialog
    if not pdf_file_path:
        pdf_file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
    
    if pdf_file_path:
        # Extract text from the PDF
        text = extract_text_from_pdf(pdf_file_path)
        
        # Ask user if they want to visualize or save the text
        choice = input("Do you want to (v)isualize the text or (s)ave it to a file? [v/s]: ").lower()
        
        if choice == 'v':
            # Visualize the text in a GUI window
            visualize_text(text, pdf_file_path)
        elif choice == 's':
            output_file_path = input("Enter output file path (or press Enter for file dialog): ")
            if not output_file_path:
                output_file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
            if output_file_path:
                save_text_to_file(text, output_file_path)
        else:
            print("\nExtracted Text:")
            print(text)
    else:
        print("No PDF file selected. Exiting.")