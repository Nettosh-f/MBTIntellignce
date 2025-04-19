# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import asyncio
import shutil
import threading
import sys
from datetime import datetime
from .extract_text import process_pdf_file
from .translation import translate_to_hebrew
from .fixed_text import insert_fixed_text
from .mbti_to_pdf import generate_mbti_report
from .utils import get_all_info, extract_mbti_qualities_scores, get_formatted_type_qualities, format_page_10_content, extract_in_preference_facets
from .consts import fixed_text_data, lines_to_remove, page_10_content


class ConsoleRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass


class MBTIProcessorGUI:
    def __init__(self, master):
        self.generate_btn = None
        self.master = master
        master.title("MBTI Processor")
        master.geometry("700x650")
        master.configure(bg="#f7f7f7")

        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.input_dir = os.path.join(self.root_dir, "input")
        os.makedirs(self.input_dir, exist_ok=True)

        self.file_path = None
        self.input_file_path = None
        self.cleaned_text_path = None
        self.translated_text_path = None
        self.fixed_text_path = None
        self.output_pdf_path = None

        self.create_widgets()

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = ConsoleRedirect(self.console_text)
        sys.stderr = ConsoleRedirect(self.console_text)

    def create_widgets(self):
        # Logo
        logo_path = os.path.join(self.root_dir, "media", "full_logo.png")
        try:
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((300, 100), Image.LANCZOS)  # LANCZOS is the replacement for ANTIALIAS
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.master, image=self.logo, bg="#f7f7f7")
            logo_label.pack(pady=10)
        except Exception as e:
            logging.warning(f"Could not load logo: {str(e)}")
            # Create a placeholder label if logo can't be loaded
            logo_label = tk.Label(self.master, text="MBTI Intelligence", font=("Helvetica", 18, "bold"), bg="#f7f7f7")
            logo_label.pack(pady=10)

        # Button Frame
        button_frame = tk.Frame(self.master, bg="#f7f7f7")
        button_frame.pack(pady=15)

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)

        self.upload_btn = ttk.Button(button_frame, text="📄 Upload File", command=self.select_file)
        self.upload_btn.grid(row=0, column=0, padx=10)

        self.generate_btn = ttk.Button(button_frame, text="⚙️ Generate Report", command=self.start_processing,
                                       state=tk.DISABLED)
        self.generate_btn.grid(row=0, column=1, padx=10)

        self.open_btn = ttk.Button(button_frame, text="📂 Open Output Folder", command=self.open_output_folder,
                                   state=tk.DISABLED)
        self.open_btn.grid(row=0, column=2, padx=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=500, mode="indeterminate")
        self.progress.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.master, text="Ready", font=("Helvetica", 10), bg="#f7f7f7", fg="#444")
        self.status_label.pack(pady=5)

        # Console Output Text Widget
        console_frame = tk.LabelFrame(self.master, text="Console Output", font=("Helvetica", 10), bg="#f7f7f7",
                                      fg="#333")
        console_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.console_text = tk.Text(console_frame, height=10, wrap="word", font=("Courier", 9), bg="#ffffff")
        self.console_text.pack(side="left", fill="both", expand=True)
        self.console_text.configure(state='disabled')

        scrollbar = ttk.Scrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.console_text['yscrollcommand'] = scrollbar.set

        # Footer
        footer = tk.Label(self.master, text="All Rights Reserved, MBTIntelligence (c), 2025",
                          font=("Helvetica", 8), bg="#f7f7f7", anchor="w", justify="left")
        footer.place(relx=0.01, rely=0.98, anchor="sw")

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file_path:
            input_filename = os.path.basename(self.file_path)
            self.input_file_path = os.path.join(self.input_dir, input_filename)
            shutil.copy2(self.file_path, self.input_file_path)

            self.generate_btn['state'] = tk.NORMAL
            self.status_label.config(text=f"Selected file: {input_filename}")
        else:
            self.status_label.config(text="Upload canceled")

    def start_processing(self):
        self.generate_btn['state'] = tk.DISABLED
        self.upload_btn['state'] = tk.DISABLED
        self.progress.start(10)
        self.status_label.config(text="Processing MBTI report...")

        threading.Thread(target=self.process_report_thread).start()

    def process_report_thread(self):
        try:
            asyncio.run(self.process_report())
            self.master.after(0, lambda: self.status_label.config(text="Processing completed successfully"))
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Error", f"An error occurred during processing: {str(e)}"))
        finally:
            self.master.after(0, self.processing_complete)

    def processing_complete(self):
        self.progress.stop()
        self.upload_btn['state'] = tk.NORMAL
        self.generate_btn['state'] = tk.NORMAL
        self.open_btn['state'] = tk.NORMAL

    async def process_report(self):
        try:
            # Step 1: Extract Text
            self.cleaned_text_path = process_pdf_file(self.file_path, lines_to_remove)
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
            mbti_type = mbti_info['type']
            mbti_type_qualities = get_formatted_type_qualities(mbti_type)
            raw_file_name = os.path.splitext(os.path.basename(self.input_file_path))[0] + "_raw.txt"
            raw_file_path = os.path.join(self.root_dir, "output", raw_file_name)
            if os.path.exists(raw_file_path):
                facets = extract_in_preference_facets(raw_file_path)
            else:
                facets = extract_in_preference_facets(self.translated_text_path)
            formatted_page_10 = format_page_10_content(page_10_content, facets)
            fixed_text_config = fixed_text_data(mbti_info, mbti_type_qualities, formatted_page_10)
            output_filename = os.path.splitext(os.path.basename(self.input_file_path))[0] + "_fixed.txt"
            self.fixed_text_path = os.path.join(output_dir, output_filename)
            insert_fixed_text(self.translated_text_path, self.fixed_text_path, fixed_text_config)

            # Step 4: Generate PDF
            output_html = os.path.join(output_dir, os.path.splitext(os.path.basename(self.input_file_path))[0] + "_report.html")
            output_pdf = os.path.join(output_dir, os.path.splitext(os.path.basename(self.input_file_path))[0] + "_report.pdf")
            logo_path = os.path.join(self.root_dir, "media", "full_logo.png")
            first_page_title = "דו&quot;ח בתרגום לעברית עבור: "
            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"Logo file not found at {logo_path}")
            generate_mbti_report(self.fixed_text_path, output_html, output_pdf, logo_path, first_page_title)
            if not os.path.exists(output_pdf):
                raise FileNotFoundError(f"Final PDF was not generated at {output_pdf}")

            self.output_pdf_path = output_pdf
            self.status_label.config(text="Report generated successfully!")
            self.master.after(0, lambda: messagebox.showinfo("Success", f"MBTI report processed successfully!\nOutput PDF: {output_pdf}"))
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Error", f"An error occurred during processing: {str(e)}"))

    def open_output_folder(self):
        output_dir = os.path.join(self.root_dir, "output")
        if os.path.exists(output_dir):
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':  # macOS
                import subprocess
                subprocess.Popen(['open', output_dir])
            else:  # Linux
                import subprocess
                subprocess.Popen(['xdg-open', output_dir])
        else:
            messagebox.showerror("Error", f"Output directory does not exist: {output_dir}")

    def process_report_wrapper(self):
        asyncio.run(self.process_report())

if __name__ == "__main__":
    root = tk.Tk()
    gui = MBTIProcessorGUI(root)
    root.mainloop()