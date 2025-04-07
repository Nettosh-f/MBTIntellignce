# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import asyncio
import shutil
from .extract_text import process_pdf_file
from .translation import translate_to_hebrew
from .fixed_text import insert_fixed_text
from .mbti_to_pdf import generate_mbti_report
from .utils import get_all_info, extract_mbti_qualities_scores,format_mbti_string
from .consts import fixed_text_data


class MBTIProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("MBTI Processor")
        master.geometry("400x200")

        self.label = tk.Label(master, text="Select MBTI PDF file to process:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.process_button = tk.Button(master, text="Process MBTI Report", command=self.process_report_wrapper, state=tk.DISABLED)
        self.process_button.pack(pady=20)

        self.file_path = None
        self.input_file_path = None
        self.cleaned_text_path = None
        self.translated_text_path = None
        self.fixed_text_path = None

        # Get the root directory of the package
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.input_dir = os.path.join(self.root_dir, "input")
        os.makedirs(self.input_dir, exist_ok=True)  # Create input directory if it doesn't exist

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            # Copy the selected file to the input directory
            input_filename = os.path.basename(self.file_path)
            self.input_file_path = os.path.join(self.input_dir, input_filename)
            shutil.copy2(self.file_path, self.input_file_path)

            self.process_button['state'] = tk.NORMAL
            self.label.config(text=f"Selected file: {input_filename}")
            messagebox.showinfo("File Copied", f"File has been copied to the input folder:\n{self.input_file_path}")

    async def process_report(self):
        try:
            # Step 1: Extract Text
            lines_to_remove_config = {
                0: [0, 1, 2, 3, 4, 5, 6, 7, 10, 11],
                1: "ALL",  # Skip entire page
                2: [0, 1, 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
                    37, 38, 39, 40, 41, 42],
                3: "ALL",
                4: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
                5: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
                6: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
                7: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                    27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
                8: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11],
                9: [0, 1, 2, 3, 4, 5, 6, 7, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
                10: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                11: [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                12: [0, 1, 2, 4, 5, 6, 7, 8, 27, 28, 29, 30, 31],
                13: [0, 1, 2, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                14: "ALL",
                15: [0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43],
                16: [0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                     29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                     60, 61, 62, 63, 64, 65, 66]
            }
            self.cleaned_text_path = process_pdf_file(self.file_path, lines_to_remove_config)
            cleaned_text_path_str = str(self.cleaned_text_path)
            if cleaned_text_path_str == "None" or not os.path.exists(cleaned_text_path_str):
                raise ValueError(f"PDF processing failed. No output file was generated at expected path: {cleaned_text_path_str}")

            # Step 2: Translate to Hebrew
            with open(self.cleaned_text_path, 'r', encoding='utf-8') as f:
                text = f.read()

            translated_text = await translate_to_hebrew(text)
            if translated_text is None:
                raise ValueError("Translation failed. No Hebrew text was generated.")
            output_dir = os.path.join(self.root_dir, "output")
            os.makedirs(output_dir, exist_ok=True)
            output_filename = os.path.splitext(os.path.basename(self.input_file_path))[0] + "_hebrew.txt"
            self.translated_text_path = os.path.join(output_dir, output_filename)
            with open(self.translated_text_path, 'w', encoding='utf-8') as f:
                f.write(translated_text)

            # Step 3: Insert Fixed Text
            mbti_info = get_all_info(self.translated_text_path)
            mbti_qualities = extract_mbti_qualities_scores(self.translated_text_path)
            mbti_page3 = format_mbti_string(mbti_qualities)
            fixed_text_config = fixed_text_data(mbti_info, mbti_page3)
            output_filename = os.path.splitext(os.path.basename(self.input_file_path))[0] + "_fixed.txt"
            self.fixed_text_path = os.path.join(output_dir, output_filename)
            insert_fixed_text(self.translated_text_path, self.fixed_text_path, fixed_text_config)

            # Step 4: Generate PDF
            output_html = os.path.join(output_dir, os.path.splitext(os.path.basename(self.input_file_path))[0] + "_report.html")
            output_pdf = os.path.join(output_dir, os.path.splitext(os.path.basename(self.input_file_path))[0] + "_report.pdf")
            logo_path = os.path.join(self.root_dir, "media", "full_logo.png")
            first_page_title = "דו״ח בתרגום לעברית עבור: "

            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"Logo file not found at {logo_path}")

            generate_mbti_report(self.fixed_text_path, output_html, output_pdf, logo_path, first_page_title)

            if not os.path.exists(output_pdf):
                raise FileNotFoundError(f"Final PDF was not generated at {output_pdf}")

            messagebox.showinfo("Success", f"MBTI report processed successfully!\nOutput PDF: {output_pdf}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")

    def process_report_wrapper(self):
        asyncio.run(self.process_report())


if __name__ == "__main__":
    root = tk.Tk()
    gui = MBTIProcessorGUI(root)
    root.mainloop()
