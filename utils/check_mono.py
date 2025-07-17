import librosa
import soundfile as sf
import os

OUTPUT_SEGMENTS_DIR = os.path.join('output', 'segments')

def check_and_convert_to_mono(directory=OUTPUT_SEGMENTS_DIR):
    """
    Check if WAV files in the specified directory are mono, convert to mono if they're not.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            filepath = os.path.join(directory, filename)
            # Load audio file
            audio, sr = librosa.load(filepath, sr=None, mono=False)
            
            # Check if stereo (has 2 channels)
            if len(audio.shape) > 1 and audio.shape[0] > 1:
                # Convert to mono by averaging channels
                audio_mono = librosa.to_mono(audio)
                # Save the mono version
                sf.write(filepath, audio_mono, sr)
                print(f"Converted {filename} to mono")
            else:
                print(f"{filename} is already mono")

if __name__ == "__main__":
    check_and_convert_to_mono() 