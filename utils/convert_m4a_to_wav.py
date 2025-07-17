import os
from pydub import AudioSegment
import shutil

RAW_DATA_DIR = os.path.join('data', 'raw')
CONVERTED_DATA_DIR = os.path.join('data', 'converted')

def convert_m4a_to_wav(filename):
    m4a_path = os.path.join(RAW_DATA_DIR, filename)
    wav_path = os.path.join(CONVERTED_DATA_DIR, os.path.splitext(filename)[0] + '.wav')
    audio = AudioSegment.from_file(m4a_path, format='m4a')
    audio.export(wav_path, format='wav')
    

def main():
    for filename in os.listdir(RAW_DATA_DIR):
        if filename.lower().endswith('.m4a'):
            convert_m4a_to_wav(filename)
        elif filename.lower().endswith('.wav'):
            src_path = os.path.join(RAW_DATA_DIR, filename)
            dst_path = os.path.join(CONVERTED_DATA_DIR, filename)
            shutil.copy2(src_path, dst_path)


if __name__ == "__main__":
    main() 