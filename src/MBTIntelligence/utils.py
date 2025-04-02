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


def get_date(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    if len(lines) >= 5:
        return lines[4].strip()
    else:
        return None


def get_all_info(file_path):
    info = {}
    info['MBTI Type'] = find_type(file_path)
    info['Name'] = get_name(file_path)
    info['Date'] = get_date(file_path)
    return info


def extract_mbti_qualities_scores(file_path):
    """
    Extract MBTI qualities and their corresponding scores from page 3 of the text file.
    This function dynamically identifies qualities regardless of their specific terms.

    Parameters:
    ----------
    file_path : str
        Path to the input text file

    Returns:
    -------
    dict
        Dictionary with MBTI qualities as keys and their scores as values
    """
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find page 3 content
    import re
    page_pattern = r'--- Page 3 ---\n(.*?)(?:--- Page 4 ---|$)'
    page_match = re.search(page_pattern, content, re.DOTALL)

    if not page_match:
        raise ValueError("Page 3 not found in the file")

    page_content = page_match.group(1)

    # Find the line with MBTI scores (looking for a line with multiple pipe symbols)
    scores_line = None
    for line in page_content.split('\n'):
        # Look for lines with multiple pipe symbols and numbers which are likely MBTI scores
        if line.count('|') >= 3 and re.search(r'\d+', line):
            scores_line = line
            break

    if not scores_line:
        raise ValueError("MBTI scores line not found in page 3")

    # Split the line by the pipe character
    parts = scores_line.split('|')
    parts = [part.strip() for part in parts]

    # Extract qualities and scores correctly
    qualities = []
    scores = []

    # Extract first quality (always at the beginning)
    qualities.append(parts[0])

    # Process middle parts which contain "score quality" format
    for i in range(1, len(parts) - 1):
        # Split the part to separate score and quality
        part = parts[i]
        # Find where the number ends and the quality begins
        match = re.match(r'(\d+)\s*(.*)', part)
        if match:
            score, quality = match.groups()
            scores.append(score)
            if quality:  # Only add if quality is not empty
                qualities.append(quality)

    # Add the last score
    if parts[-1].strip().isdigit():
        scores.append(parts[-1])

    # Ensure we have equal number of qualities and scores
    min_len = min(len(qualities), len(scores))

    # Create mapping of qualities to scores
    qualities_scores = {}
    for i in range(min_len):
        qualities_scores[qualities[i]] = int(scores[i])

    return qualities_scores
