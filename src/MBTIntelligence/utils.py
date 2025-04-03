import re
from typing import Optional, Dict, List
try:
    from .consts import MBTI_TYPES, MBTI_QUALITIES, MBTI_TYPE_QUALITIES
except ImportError:
    from consts import MBTI_TYPES, MBTI_QUALITIES, MBTI_TYPE_QUALITIES


def find_type(file_path: str) -> Optional[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    for mbti_type in MBTI_TYPES:
        if mbti_type in content:
            return mbti_type
    return None


def get_name(file_path: str) -> Optional[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        file.readline()
        second_line = file.readline().strip()
        return second_line if second_line else None


def get_date(file_path: str) -> Optional[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Hebrew date pattern: day month year
    hebrew_date_pattern = r'\d{1,2}\s+ב?[א-ת]+\s+\d{4}'

    date_match = re.search(hebrew_date_pattern, content)
    return date_match.group() if date_match else None


def get_all_info(file_path: str) -> Dict[str, Optional[str]]:
    info = {
        'name': get_name(file_path),
        'date': get_date(file_path),
        'type': find_type(file_path)
    }
    return info


def extract_mbti_qualities_scores(file_path: str) -> Dict[str, int]:
    qualities_scores = {quality: 0 for quality in MBTI_QUALITIES}
    mbti_type = find_type(file_path)

    if mbti_type:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Pattern to match a line with מוחצנות or מופנמות and extract all numbers
        pattern = r'(מוחצנות|מופנמות).*?(\d+).*?(\d+).*?(\d+).*?(\d+)'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            qualities = ['Extraversion', 'Sensing', 'Thinking', 'Judging']
            for i, quality in enumerate(qualities):
                qualities_scores[quality] = int(match.group(i + 2))

    return qualities_scores


if  __name__ == "__main__":
    file_path = r"F:\projects\MBTInteligence\output\nir-bensinai-MBTI_hebrew.txt"  # Replace with your file path
    info = get_all_info(file_path)
    print(f"Name: {info['name']}")
    print(f"Date: {info['date']}")
    print(f"MBTI Type: {info['type']}")

    qualities_scores = extract_mbti_qualities_scores(file_path)
    print("MBTI Qualities Scores:")
    for quality, score in qualities_scores.items():
        print(f"{quality}: {score}")