import re


def find_type(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression pattern to match 4 capital letters that are not "MBTI"
    pattern = r'(?!MBTI)[A-Z]{4}'
    match = re.search(pattern, content)

    if match:
        return match.group()
    else:
        return None


def get_name(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    if len(lines) >= 4:
        return lines[3].strip()
    else:
        return None


if __name__ == '__main__':
    print(find_type(r'F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI-cleaned-hebrew.txt'))  # Output: ABC1
    print(get_name(
        r'F:\projects\MBTInteligence\MBTItranslated\nir-bensinai-MBTI-cleaned-hebrew.txt'))  # Output: nir-bensinai-MBTI-cleaned-hebrew
