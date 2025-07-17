# Whisper WelzijnAI: Audio Segmentation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   You may also need to install ffmpeg on your system (e.g., `brew install ffmpeg` on macOS).

2. Place your original audio files in the `data` folder (create it if it doesn't exist).

## Usage

Run the segmentation script:

```bash
python segment_audio.py
```

Segmented audio files (max 30s, speech only) will be saved in the `output` folder.

## Notes
- The first run of the script will prompt you to log in to HuggingFace to download the VAD model.
- Supported audio formats: wav, mp3, flac, ogg, m4a. 