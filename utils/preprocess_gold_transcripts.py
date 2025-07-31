import os
import re
import string

def process_gold_transcripts(reference_folder=os.path.join('data', 'reference_transcripts_beatrix')):
    """
    Process gold standard transcriptions:
    1. Write a copy to 'orthographic_clean' with leading whitespace stripped and all instances of 'uh', 'eh', 'ehm', 'oh' removed, ensure no whitespace before a final period, and no more than one whitespace between words.
    2. Write a copy to 'normalized' with leading whitespace stripped, keeping instances of 'uh', 'eh', 'ehm', 'oh', but with punctuation removed, lowercased, and no more than one whitespace between words.
    3. Write a copy to 'normalized_clean' with leading whitespace stripped, fillers removed, punctuation removed, lowercased, and no more than one whitespace between words.
    """
    # Derive subdirectories from the reference folder
    ortho_dir = os.path.join(reference_folder, 'orthographic')
    ortho_clean_dir = os.path.join(reference_folder, 'orthographic_clean')
    normalized_dir = os.path.join(reference_folder, 'normalized')
    normalized_clean_dir = os.path.join(reference_folder, 'normalized_clean')
    
    # Ensure all directories exist
    os.makedirs(ortho_dir, exist_ok=True)
    os.makedirs(ortho_clean_dir, exist_ok=True)
    os.makedirs(normalized_dir, exist_ok=True)
    os.makedirs(normalized_clean_dir, exist_ok=True)

    fillers = [r'\buh\b', r'\beh\b', r'\behm\b', r'\boh\b']
    fillers_pattern = re.compile('|'.join(fillers), re.IGNORECASE)
    punctuation_pattern = re.compile(f'[{re.escape(string.punctuation)}]')
    whitespace_pattern = re.compile(r'\s+')  # one or more whitespace
    space_before_period_pattern = re.compile(r'\s+\.$')

    for fname in os.listdir(ortho_dir):
        if not fname.endswith('.txt'):
            continue
        src_path = os.path.join(ortho_dir, fname)
        # Read lines from the orthographic file
        with open(src_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Strip leading whitespace from all lines
        stripped_lines = [line.lstrip() for line in lines]

        # 1. Write to orthographic_clean: remove leading whitespace and fillers
        clean_lines = [fillers_pattern.sub('', line) for line in stripped_lines]
        # Remove whitespace before a final period
        clean_lines = [space_before_period_pattern.sub('.', l) for l in clean_lines]
        # Collapse all whitespace to a single space and strip leading/trailing whitespace
        clean_lines = [whitespace_pattern.sub(' ', l).strip() + ('\n' if l.endswith('\n') else '') for l in clean_lines]
        clean_path = os.path.join(ortho_clean_dir, fname)
        with open(clean_path, 'w', encoding='utf-8') as f:
            f.writelines(clean_lines)

        # 2. Write to normalized: keep fillers, remove punctuation, lowercase
        norm_lines = [punctuation_pattern.sub('', line).lower() for line in stripped_lines]
        # Collapse all whitespace to a single space and strip leading/trailing whitespace
        norm_lines = [whitespace_pattern.sub(' ', l).strip() + ('\n' if l.endswith('\n') else '') for l in norm_lines]
        norm_path = os.path.join(normalized_dir, fname)
        with open(norm_path, 'w', encoding='utf-8') as f:
            f.writelines(norm_lines)

        # 3. Write to normalized_clean: remove fillers, punctuation, lowercase
        norm_clean_lines = [punctuation_pattern.sub('', fillers_pattern.sub('', line)).lower() for line in stripped_lines]
        # Collapse all whitespace to a single space and strip leading/trailing whitespace
        norm_clean_lines = [whitespace_pattern.sub(' ', l).strip() + ('\n' if l.endswith('\n') else '') for l in norm_clean_lines]
        norm_clean_path = os.path.join(normalized_clean_dir, fname)
        with open(norm_clean_path, 'w', encoding='utf-8') as f:
            f.writelines(norm_clean_lines)

    print(f"Processed files from: {ortho_dir}\n  Orthographic_clean: {ortho_clean_dir}\n  Normalized: {normalized_dir}\n  Normalized_clean: {normalized_clean_dir}") 