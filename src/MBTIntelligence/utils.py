import re
from typing import Optional, Dict, List

try:
    from .consts import MBTI_TYPES, MBTI_QUALITIES, MBTI_TYPE_QUALITIES, MBTI_QUALITIES_HEBREW
except ImportError:
    from consts import MBTI_TYPES, MBTI_QUALITIES, MBTI_TYPE_QUALITIES, MBTI_QUALITIES_HEBREW


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


def format_mbti_string(mbti_qualities: Dict[str, int]) -> str:
    if not isinstance(mbti_qualities, dict):
        return "Invalid input: expected a dictionary"

    formatted_items = []
    for quality, score in mbti_qualities.items():
        if score != 0:  # Only include qualities with non-zero scores
            hebrew_quality = MBTI_QUALITIES_HEBREW.get(quality, quality)  # Use English if Hebrew not found
            formatted_items.append(f"{hebrew_quality}: {score}")

    return " | ".join(formatted_items)


def extract_mbti_qualities_scores(file_path: str) -> Dict[str, int]:
    qualities_scores = {quality: 0 for quality in MBTI_QUALITIES}
    mbti_type = find_type(file_path)
    print(qualities_scores)
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


def collect_preferred_qualities(file_path: str) -> List[str]:
    preferred_qualities = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Pattern to match qualities with "in-preference"
        pattern = r'\*\*([\w\s]+)\*\*\s*\(in-preference\)'

        # Find all matches
        matches = re.findall(pattern, content)

        # Add matches to the list
        preferred_qualities.extend(matches)

        print(f"Found {len(preferred_qualities)} preferred qualities.")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {str(e)}")

    return preferred_qualities


def get_formatted_type_qualities(mbti_type: str) -> List[str]:
    """
    Returns a list of formatted qualities (English and Hebrew) for a given MBTI type.

    Args:
        mbti_type: A string representing the MBTI type (e.g., 'INTJ', 'ENFP')

    Returns:
        A list of strings representing the formatted qualities for the given type,
        in the format "Quality_English (Quality_Hebrew)".
        Returns an empty list if the type is not found.
    """
    if not mbti_type or mbti_type not in MBTI_TYPES:
        return []

    # Get the qualities associated with this type
    qualities = MBTI_TYPE_QUALITIES.get(mbti_type, [])

    # Format each quality with both English and Hebrew
    formatted_qualities = []
    for quality in qualities:
        hebrew_quality = MBTI_QUALITIES_HEBREW.get(quality, "")
        formatted_qualities.append(f"{quality} ({hebrew_quality})")

    return formatted_qualities


if __name__ == '__main__':
    file_path = r'F:\projects\MBTInteligence\output\nir-bensinai-MBTI_fixed.txt'
    print(collect_preferred_qualities(file_path))
    mbti_type = find_type(file_path)
    print(mbti_type)
    print(get_formatted_type_qualities(mbti_type))
    mbti_type_qualities = MBTI_TYPE_QUALITIES.get(mbti_type, [])
    print(MBTI_TYPE_QUALITIES.get(mbti_type, [])[1])
    print(extract_mbti_qualities_scores(file_path))
