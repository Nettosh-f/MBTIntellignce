import tkinter as tk
from tkinter import filedialog, messagebox
import os
import asyncio
from .extract_text import process_pdf_file
from .translation import translate_to_hebrew
from .fixed_text import insert_fixed_text
from .mbti_to_pdf import generate_mbti_report


class MBTIProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("MBTI Processor")
        master.geometry("400x300")

        self.label = tk.Label(master, text="Select MBTI PDF file to process:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.extract_button = tk.Button(master, text="1. Extract Text", command=self.extract_text, state=tk.DISABLED)
        self.extract_button.pack(pady=5)

        self.translate_button = tk.Button(master, text="2. Translate to Hebrew", command=self.translate_text, state=tk.DISABLED)
        self.translate_button.pack(pady=5)

        self.insert_fixed_text_button = tk.Button(master, text="3. Insert Fixed Text", command=self.insert_fixed_text, state=tk.DISABLED)
        self.insert_fixed_text_button.pack(pady=5)

        self.generate_pdf_button = tk.Button(master, text="4. Generate PDF", command=self.generate_pdf, state=tk.DISABLED)
        self.generate_pdf_button.pack(pady=5)

        self.file_path = None
        self.cleaned_text_path = None
        self.translated_text_path = None
        self.fixed_text_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            self.extract_button['state'] = tk.NORMAL
            self.label.config(text=f"Selected file: {os.path.basename(self.file_path)}")

    def extract_text(self):
        try:
            lines_to_remove_config = {
                0: [0, 1, 2, 3, 4, 5, 6, 7],
                1: "ALL",  # Skip entire page
                2: [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
                    37,
                    38, 39, 40],
                3: "ALL",
                4: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27,
                    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
                5: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27,
                    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
                6: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27,
                    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27,
                    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
                8: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
                9: [0, 1, 2, 3, 4, 5, 6, 7, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
                10: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                11: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                12: [0, 1, 2, 4, 5, 6, 7, 8, 27, 28, 29, 30, 31],
                13: [0, 1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                14: "ALL",
                15: [0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                     31,
                     32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
                16: [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                     29,
                     30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                     61, 62, 63, 64, 65, 66]
            }
            self.cleaned_text_path = process_pdf_file(self.file_path, lines_to_remove_config)
            cleaned_text_path_str = str(self.cleaned_text_path)
            if cleaned_text_path_str == "None" or not os.path.exists(cleaned_text_path_str):
                raise ValueError(f"PDF processing failed. No output file was generated at expected path: {cleaned_text_path_str}")

            messagebox.showinfo("Success", f"Text extracted successfully.\nOutput: {cleaned_text_path_str}")
            self.translate_button['state'] = tk.NORMAL
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during text extraction: {str(e)}")

    async def translate_text_async(self):
        try:
            with open(self.cleaned_text_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            translated_text = await translate_to_hebrew(text)
            
            if translated_text is None:
                raise ValueError("Translation failed. No Hebrew text was generated.")
            
            self.translated_text_path = os.path.splitext(self.cleaned_text_path)[0] + "-hebrew.txt"
            with open(self.translated_text_path, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            
            messagebox.showinfo("Success", f"Text translated successfully.\nOutput: {self.translated_text_path}")
            self.insert_fixed_text_button['state'] = tk.NORMAL
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during translation: {str(e)}")

    def translate_text(self):
        asyncio.run(self.translate_text_async())

    def insert_fixed_text(self):
        try:
            fixed_text_config = {
                # ... (define your fixed text configuration here)
            }
            self.fixed_text_path = os.path.splitext(self.translated_text_path)[0] + "-fixed.txt"
            insert_fixed_text(self.translated_text_path, self.fixed_text_path, fixed_text_config)
            
            messagebox.showinfo("Success", f"Fixed text inserted successfully.\nOutput: {self.fixed_text_path}")
            self.generate_pdf_button['state'] = tk.NORMAL
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while inserting fixed text: {str(e)}")

    def generate_pdf(self):
        try:
            output_html = os.path.splitext(self.file_path)[0] + "_report.html"
            output_pdf = os.path.splitext(self.file_path)[0] + "_report.pdf"
            logo_path = r"F:\projects\MBTInteligence\media\full_logo.png"
            
            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"Logo file not found at {logo_path}")
            
            generate_mbti_report(self.fixed_text_path, output_html, output_pdf, logo_path)

            if not os.path.exists(output_pdf):
                raise FileNotFoundError(f"Final PDF was not generated at {output_pdf}")

            messagebox.showinfo("Success", f"PDF generated successfully!\nOutput PDF: {output_pdf}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the PDF: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = MBTIProcessorGUI(root)
    root.mainloop()