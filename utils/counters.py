import os
import librosa
import re

def count_total_words(folder_path):
    """
    Count the total number of words and punctuation symbols across all .txt files in a folder.
    
    Args:
        folder_path (str): Path to the folder containing .txt files
        
    Returns:
        int: Total token count (words + punctuation symbols) across all .txt files
    """
    total_tokens = 0
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist")
        return 0
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Split on whitespace first, then split each word on punctuation
                    words = content.split()
                    for word in words:
                        # Split word on punctuation boundaries while keeping punctuation as separate tokens
                        tokens = re.findall(r'\w+|[^\w\s]', word)
                        total_tokens += len(tokens)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return total_tokens

def get_total_audio_duration(folder_path):
    """
    Calculate the total duration of all audio files in a folder.
    
    Args:
        folder_path (str): Path to the folder containing audio files
        
    Returns:
        float: Total duration in seconds across all audio files
    """
    total_duration = 0.0
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist")
        return 0.0
    
    # Audio file extensions to look for
    audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac']
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in audio_extensions:
            file_path = os.path.join(folder_path, filename)
            try:
                duration = librosa.get_duration(path=file_path)
                total_duration += duration
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return total_duration 