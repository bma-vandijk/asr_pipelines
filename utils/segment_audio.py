import os, torch
from pydub import AudioSegment
from pyannote.audio import Pipeline

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
MAX_SEGMENT_LENGTH = 30 * 1000  # 30 seconds in milliseconds

# Read API key from .secrets/hf_api_key.txt
with open(os.path.join('.secrets', 'hf_api_key.txt'), 'r') as file:
    AUTH_TOKEN = file.read().strip()

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize pyannote speaker diarization pipeline (requires HuggingFace token for first use)
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=AUTH_TOKEN)  # Set your HF token if needed

pipeline.to(torch.device("mps"))

def segment_audio_file(file_path, output_dir):
    audio = AudioSegment.from_file(file_path)
    basename = os.path.splitext(os.path.basename(file_path))[0]
    # Diarization with two speakers
    diarization = pipeline(file_path, num_speakers=2)
    # Collect segments by speaker
    speaker_segments = {}
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if speaker not in speaker_segments:
            speaker_segments[speaker] = []
        speaker_segments[speaker].append((turn.start, turn.end))
    # For each speaker, segment their speech into max 30s chunks
    for speaker, segments in speaker_segments.items():
        seg_idx = 0
        for start, end in segments:
            start_ms = int(start * 1000)
            end_ms = int(end * 1000)
            for chunk_start in range(start_ms, end_ms, MAX_SEGMENT_LENGTH):
                chunk_end = min(chunk_start + MAX_SEGMENT_LENGTH, end_ms)
                segment = audio[chunk_start:chunk_end]
                segment.export(os.path.join(output_dir, f"{basename}_{speaker}_seg_{seg_idx}.wav"), format="wav")
                seg_idx += 1

def main():
    for filename in os.listdir(DATA_DIR):
        if filename.lower().endswith(('.wav', '.mp3', '.flac', '.ogg', '.m4a')):
            file_path = os.path.join(DATA_DIR, filename)
            segment_audio_file(file_path, OUTPUT_DIR)

if __name__ == "__main__":
    main() 