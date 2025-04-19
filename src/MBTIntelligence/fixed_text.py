import re
import chardet
# from .utils import get_all_info, extract_mbti_qualities_scores
# from .consts import MBTI_QUALITIES_HEBREW, fixed_text_data


def insert_fixed_text(input_file, output_file, page_line_text_map):
    try:
        # Detect the file encoding
        with open(input_file, 'rb') as f:
            raw_data = f.read()
        detected = chardet.detect(raw_data)
        file_encoding = detected['encoding']
        print(f"Detected encoding for input file: {file_encoding}")

        # Read the file with the detected encoding
        with open(input_file, 'r', encoding=file_encoding, errors='replace') as f:
            lines = f.readlines()

        current_page = 0
        line_count_in_page = 0
        result_lines = []

        for line in lines:
            # Check if this is a page delimiter line
            if line.strip().startswith('--- Page ') and line.strip().endswith('---'):
                # Extract the page number
                try:
                    page_str = line.strip().replace('--- Page ', '').replace(' ---', '')
                    current_page = int(page_str)
                    # Reset line count for the new page
                    line_count_in_page = 0
                except ValueError:
                    pass

                # Add the page delimiter line to results
                result_lines.append(line)
                continue

            # Increment line count
            line_count_in_page += 1

            # Check if we need to insert fixed text before this line
            if current_page in page_line_text_map and line_count_in_page in page_line_text_map[current_page]:
                text_to_insert = page_line_text_map[current_page][line_count_in_page]
                if isinstance(text_to_insert, str) and "DELETE" in text_to_insert:
                    # print(f"Deleted line at Page {current_page}, Line {line_count_in_page}: {line.strip()[:30]}...")
                    continue
                else:
                    # Handle both string and list inputs
                    if isinstance(text_to_insert, list):
                        result_lines.extend([t + '\n' for t in text_to_insert])
                    else:
                        result_lines.append(text_to_insert + '\n')
                    # print(f"Inserted text at Page {current_page}, Line {line_count_in_page}: {text_to_insert[:30]}...")

            # Add the original line
            result_lines.append(line)

        # Write the modified content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(result_lines)
        print(f"Successfully processed the file. Output saved to {output_file}")
    except Exception as e:
        print(f"Error in insert_fixed_text: {str(e)}")
        raise


if __name__ == "__main__":
    from utils import get_all_info, extract_mbti_qualities_scores, format_mbti_string
    from consts import fixed_text_data
    input_file = r"F:\projects\MBTInteligence\output\nir-bensinai-MBTI_hebrew.txt"
    output_file = r"F:\projects\MBTInteligence\output\output.txt"
    mbti_info = get_all_info(input_file)
    mbti_qualities = extract_mbti_qualities_scores(input_file)
    mbti_page3 = format_mbti_string(mbti_qualities)
    fixed_text_config = fixed_text_data(mbti_info, mbti_page3)
    insert_fixed_text(input_file, output_file, fixed_text_config)