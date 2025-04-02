import re
from typing import Optional, Dict, List
from .consts import MBTI_TYPES, MBTI_QUALITIES, MBTI_TYPE_QUALITIES


def find_type(file_path: str) -> Optional[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    for mbti_type in MBTI_TYPES:
        if mbti_type in content:
            return mbti_type
    return None


def get_name(file_path: str) -> Optional[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines[3].strip() if len(lines) >= 4 else None


def get_date(file_path: str) -> Optional[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    date_match = re.search(r'\d{2}/\d{2}/\d{4}', content)
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
        type_qualities = MBTI_TYPE_QUALITIES[mbti_type]
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        for quality in type_qualities:
            match = re.search(rf'{quality}\s+(\d+)', content)
            if match:
                qualities_scores[quality] = int(match.group(1))

    return qualities_scores
