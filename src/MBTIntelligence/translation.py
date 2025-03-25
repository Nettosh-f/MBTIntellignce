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
    prompt = (
        f"You are a professional english-hebrew translator and a proficient in MBTI terminology."
        f" Translate the following text to Hebrew:\n{text}, make sure to output nothing but the translated text. "
        f"wherever it is necessary. whenever possible, split all to 120 caracter per line, without shortening or losing"
        f" meaning. make sure all information makes sense to read.")
    response = model.generate_content(prompt, generation_config={"temperature": 0.0})
    end_time = time.time()
    response_time = end_time - start_time
    print(response.usage_metadata)
    print(f"Response time: {response_time * 1000:.4f} miliseconds")

    return response.text


def main():
    file_path = r"F:\projects\MBTInteligence\MBTItxt\nir-bensinai-MBTI-cleaned.txt"  # Change to your file path
    text = read_text_file(file_path)
    translated_text = translate_to_hebrew(text)

    # Save the Hebrew output to a new file
    filename = os.path.splitext(os.path.basename(file_path))[0] + "-hebrew.txt"
    output_path = os.path.join(r"F:\projects\MBTInteligence\MBTItranslated", filename)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(translated_text)

    print(f"Translated text saved to {output_path}")


if __name__ == "__main__":
    main()
