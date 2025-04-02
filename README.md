# MBTIntelligence - MBTI Report Processor

MBTIntelligence is a Python application designed to process Myers-Briggs Type Indicator (MBTI) personality assessment reports. It provides a graphical user interface for extracting text from PDF reports, translating the content to Hebrew, inserting fixed text, and generating a final PDF report.

## Features

- Extract text from single or multiple MBTI report PDF files
- Automatically save extracted text to .txt files for further analysis
- Preserve page structure with page number indicators
- Translate extracted text to Hebrew using OpenAI's GPT model
- Insert fixed text into translated content
- Generate a final PDF report with custom formatting
- User-friendly graphical interface
- Handle errors gracefully

## Requirements

- Python 3.7+
- tkinter
- PyPDF2
- openai
- python-dotenv
- (Any other dependencies your project uses)

## Installation

1. Clone this repository:
```commandline
  git clone https://github.com/Nettosh-f/MBTIntellignce
  cd MBTIntelligence
```
2. Ensure you have Python installed on your system

3. Install the required packages:

4. Set up your OpenAI API key:
- Create a `.env` file in the project root directory
- Add your OpenAI API key to the file:
  ```
  OPENAI_API_KEY=your_api_key_here
  ```

## Usage

1. Run the application:

```commandline
   python run.py
```

2. Use the graphical interface to process MBTI reports:
- Click "Select File" to choose an MBTI PDF report
- Click "Extract Text" to extract the content from the PDF
- Click "Translate to Hebrew" to translate the extracted text
- Click "Insert Fixed Text" to add predefined content to the translation
- Click "Generate PDF" to create the final report

## Project Structure

- `run.py`: The entry point of the application
- `src/MBTIntelligence/`:
  - `main.py`: Contains the main GUI class and application logic
  - `extract_text.py`: Handles PDF text extraction
  - `translation.py`: Manages the translation process using OpenAI's API
  - `fixed_text.py`: Handles insertion of predefined text
  - `mbti_to_pdf.py`: Generates the final PDF report
  - `consts.py`: Stores constant values and prompts
- `media/`: Contains assets like logos used in the report

## Customization

- To modify the fixed text insertion, edit the `fixed_text_config` in `main.py`
- To change the translation prompt, update `SYSTEM_PROMPT` in `consts.py`
- To adjust PDF formatting, modify the `generate_mbti_report` function in `mbti_to_pdf.py`

## Troubleshooting

- If you encounter issues with file paths, ensure that all directory references in the code match your project structure
- For OpenAI API errors, check that your API key is correctly set in the `.env` file
- If PDF generation fails, verify that all required fonts and assets are present in the specified locations

## Contributing

Contributions to MBTIntelligence are welcome! Please feel free to submit pull requests, create issues or spread the word.

## License

[Include your chosen license here]

## Acknowledgements

This project uses the following open-source libraries:
- PyPDF2 for PDF processing
- OpenAI's GPT model for translation
- [List any other major libraries or resources you've used]

## Contact

For any queries or support, please open an issue on the GitHub repository or contact [your contact information].
