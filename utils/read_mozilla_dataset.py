import os
import pandas as pd
import shutil
from pathlib import Path

def create_orthographic_files(tsv_path, n_rows=None, seed=None):
    # Read the TSV file
    df = pd.read_csv(tsv_path, sep='\t')
    
    # Filter for sixties
    df = df[df['age'] == 'sixties']
    
    # Set seed if provided
    if seed is not None:
        df = df.sample(n=min(n_rows, len(df)) if n_rows else len(df), random_state=seed)
    elif n_rows is not None:
        df = df.sample(n=min(n_rows, len(df)))
    
    output_dir = os.path.join('data', 'reference_transcripts_mozilla', 'orthographic')
    os.makedirs(output_dir, exist_ok=True)
    
    for _, row in df.iterrows():
        filename = row['path'].replace('.mp3', '.txt')
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(row['sentence'])

def copy_audio_from_transcripts(transcript_folder_path, audio_folder_path):
    """
    Create a list of all transcripts in a folder and copy corresponding audio files.
    
    Args:
        transcript_folder_path (str): Path to folder containing transcript files
        audio_folder_path (str): Path to folder containing audio files
    
    Returns:
        list: List of transcript filenames that were processed
    """
    # Create output directory
    output_dir = os.path.join('output', 'segments_mozilla')
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of all transcript files
    transcript_files = []
    for filename in os.listdir(transcript_folder_path):
        if filename.endswith('.txt'):
            transcript_files.append(filename)
    
    print(f"Found {len(transcript_files)} transcript files")
    
    # Copy corresponding audio files
    copied_files = []
    for transcript_file in transcript_files:
        # Get base filename without extension
        base_filename = os.path.splitext(transcript_file)[0]
        
        # Look for audio files with the same base filename but different extensions
        audio_found = False
        for audio_file in os.listdir(audio_folder_path):
            audio_base = os.path.splitext(audio_file)[0]
            if audio_base == base_filename:
                # Found matching audio file
                audio_filepath = os.path.join(audio_folder_path, audio_file)
                output_filepath = os.path.join(output_dir, audio_file)
                shutil.copy2(audio_filepath, output_filepath)
                copied_files.append(audio_file)
                print(f"Copied: {audio_file}")
                audio_found = True
                break
        
        if not audio_found:
            print(f"Warning: Audio file not found for transcript: {transcript_file}")
    
    print(f"Successfully copied {len(copied_files)} audio files to {output_dir}")
    