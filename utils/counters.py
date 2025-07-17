import os
import librosa

def count_total_words(folder_path):
    """
    Count the total number of words across all .txt files in a folder.
    
    Args:
        folder_path (str): Path to the folder containing .txt files
        
    Returns:
        int: Total word count across all .txt files
    """
    total_words = 0
    
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
                    words = content.split()
                    total_words += len(words)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return total_words

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