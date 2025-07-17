import os
import re
import string

REFERENCE_TRANSCRIPTS_DIR = os.path.join('data', 'reference_transcripts')
ORTHO_DIR = os.path.join(REFERENCE_TRANSCRIPTS_DIR, 'orthographic')
ORTHO_CLEAN_DIR = os.path.join(REFERENCE_TRANSCRIPTS_DIR, 'orthographic_clean')
NORMALIZED_DIR = os.path.join(REFERENCE_TRANSCRIPTS_DIR, 'normalized')

def process_gold_transcripts(src_dir=ORTHO_DIR):
    """
    Process gold standard transcriptions:
    1. Overwrite each file in src_dir with leading whitespace stripped from each line.
    2. Write a copy to 'orthographic_clean' with leading whitespace and all instances of 'uh', 'eh', 'ehm', 'oh' removed, ensure no whitespace before a final period, and no more than one whitespace between words.
    3. Write a copy to 'normalized' with leading whitespace, all instances of 'uh', 'eh', 'ehm', 'oh', and all punctuation removed, lowercased, and no more than one whitespace between words.
    """
    # Ensure all directories exist
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(ORTHO_CLEAN_DIR, exist_ok=True)
    os.makedirs(NORMALIZED_DIR, exist_ok=True)

    fillers = [r'\buh\b', r'\beh\b', r'\behm\b', r'\boh\b']
    fillers_pattern = re.compile('|'.join(fillers), re.IGNORECASE)
    punctuation_pattern = re.compile(f'[{re.escape(string.punctuation)}]')
    whitespace_pattern = re.compile(r'\s+')  # one or more whitespace
    space_before_period_pattern = re.compile(r'\s+\.$')

    for fname in os.listdir(src_dir):
        if not fname.endswith('.txt'):
            continue
        src_path = os.path.join(src_dir, fname)
        # Read lines from the orthographic file
        with open(src_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 1. Overwrite original in orthographic: strip leading whitespace
        stripped_lines = [line.lstrip() for line in lines]
        with open(src_path, 'w', encoding='utf-8') as f:
            f.writelines(stripped_lines)

        # 2. Write to orthographic_clean: remove leading whitespace and fillers (from stripped lines)
        clean_lines = [fillers_pattern.sub('', line) for line in stripped_lines]
        # Remove whitespace before a final period
        clean_lines = [space_before_period_pattern.sub('.', l) for l in clean_lines]
        # Collapse all whitespace to a single space and strip leading/trailing whitespace
        clean_lines = [whitespace_pattern.sub(' ', l).strip() + ('\n' if l.endswith('\n') else '') for l in clean_lines]
        clean_path = os.path.join(ORTHO_CLEAN_DIR, fname)
        with open(clean_path, 'w', encoding='utf-8') as f:
            f.writelines(clean_lines)

        # 3. Write to normalized: remove fillers, punctuation, and lowercase (from stripped lines)
        norm_lines = [punctuation_pattern.sub('', fillers_pattern.sub('uh', line)).lower() for line in stripped_lines]
        # Collapse all whitespace to a single space and strip leading/trailing whitespace
        norm_lines = [whitespace_pattern.sub(' ', l).strip() + ('\n' if l.endswith('\n') else '') for l in norm_lines]
        norm_path = os.path.join(NORMALIZED_DIR, fname)
        with open(norm_path, 'w', encoding='utf-8') as f:
            f.writelines(norm_lines)

    print(f"Processed files from: {src_dir}\n  Orthographic_clean: {ORTHO_CLEAN_DIR}\n  Normalized: {NORMALIZED_DIR}") 