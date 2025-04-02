from dotenv import load_dotenv
from openai import OpenAI
import os
import time

from consts import SYSTEM_PROMPT
print(SYSTEM_PROMPT)

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)


def read_text_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()


def translate_to_hebrew(text):
    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.0,
            top_p=1.0,
            max_tokens=16384
        )
        end_time = time.time()
        response_time = end_time - start_time

        # Token usage information
        request_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        print(f"Response time: {response_time * 1000:.4f} milliseconds")
        print(f"Request tokens: {request_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(f"Total tokens: {total_tokens}")

        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def main():
    file_path = r"F:\projects\MBTInteligence\MBTItxt\asaf-solomon-267149-4ae2ac9c-005e-ef11-bdfd-6045bd04b01a-cleaned.txt"
    text = read_text_file(file_path)
    translated_text = translate_to_hebrew(text)

    if translated_text:
        # Save the Hebrew output without fixed text
        filename = os.path.splitext(os.path.basename(file_path))[0] + "-hebrew.txt"
        output_path = os.path.join(r"F:\projects\MBTInteligence\MBTItranslated", filename)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(translated_text)
        print(f"Translated text saved to {output_path}")
    else:
        print("Translation failed.")


if __name__ == "__main__":
    main()
