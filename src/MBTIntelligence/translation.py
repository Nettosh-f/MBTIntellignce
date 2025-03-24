from dotenv import load_dotenv
import google.generativeai as genai
import os
import time

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)


def read_text_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()


def translate_to_hebrew(text):
    start_time = time.time()
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = (f"you are now a professional MBTI life coach, and a world grade english-hebrew translator."
              f"the following text has been extracted from an MBTI report using pypdf2 :{text}, translate it to hebrew."
              f"make sure to return it in a JSON format. keep the page numbers as a key value. "
              f"in pages where there used to be a table, organize the text into a sub values, so it can be placed "
              f"into a new pdf seamlessly.")
        # f"Translate the following text to Hebrew:\n{text}, please remove all unnecessary page header and footers.",
        # "make sure to output nothing but the translated text. do not translate or include page 1 in your response. ",
        # "include a title with the name of the reciever, in page 5-9, the structure is of a table, where all the text "
        # "was read by pypdf2 from left to right, structure it in a logical way. return the answer in JSON for such that each page "
        # "has a 'page{number}' key.")
    response = model.generate_content(prompt, generation_config={"temperature": 0.0})
    end_time = time.time()
    response_time = end_time - start_time
    print(response.usage_metadata)
    print(f"Response time: {response_time * 1000:.4f} miliseconds")

    return response.text


def main():
    file_path = "../../MBTItxt/nir-bensinai-MBTI_cleaned.txt"  # Change to your file path
    text = read_text_file(file_path)
    translated_text = translate_to_hebrew(text)

    # Save the Hebrew output to a new file
    filename = os.path.splitext(os.path.basename(file_path))[0] + "_hebrew.txt"
    output_path = os.path.join("../../MBTItranslated", filename)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(translated_text)

    print(f"Translated text saved to {output_path}")


if __name__ == "__main__":
    main()
