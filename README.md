# Whisper WelzijnAI: Audio Processing and Transcription Pipeline

This repository contains a comprehensive audio processing and transcription pipeline designed for Dutch speech recognition, particularly focused on elderly care conversations. The system processes audio files through segmentation, transcription using various ASR models, and evaluation against reference transcripts.

## 🏗️ Project Structure

```
whisper_welzijnAI/
├── data/
│   ├── raw/                    # Original audio files (m4a, wav, etc.)
│   ├── converted/              # Converted audio files (wav format)
│   └── reference_transcripts/  # Gold standard transcripts
│       ├── orthographic/       # Original reference transcripts
│       ├── orthographic_clean/ # Cleaned reference transcripts
│       └── normalized/         # Normalized reference transcripts
├── output/
│   ├── segments/               # Audio segments (max 30s each)
│   └── transcripts/            # ASR model outputs
│       ├── whisper-large-v2/
│       ├── whisper-large-v3/
│       ├── whisper-medium/
│       ├── whisper-small/
│       └── [other models]/
├── utils/                      # Processing scripts
└── .secrets/                   # API keys (not in git)
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Install additional system dependencies
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg
```

### 2. Configure API Keys

Create a `.secrets/hf_api_key.txt` file with your HuggingFace API token:
```bash
mkdir -p .secrets
echo "your_huggingface_token_here" > .secrets/hf_api_key.txt
```

### 3. Prepare Your Data

Place your audio files in the `data/raw/` directory. Supported formats: `wav`, `mp3`, `flac`, `ogg`, `m4a`.

## 🔧 Utility Scripts

The `utils/` folder contains specialized scripts for different stages of the audio processing pipeline:

### 1. Audio Conversion (`convert_m4a_to_wav.py`)

**Purpose**: Converts audio files from various formats (especially m4a) to WAV format for consistent processing.

**What it does**:
- Reads audio files from `data/raw/`
- Converts m4a files to WAV format
- Copies existing WAV files to `data/converted/`
- Ensures all audio files are in a consistent format

**Usage**:
```bash
python utils/convert_m4a_to_wav.py
```

### 2. Audio Segmentation (`segment_audio.py`)

**Purpose**: Splits long audio files into shorter segments (max 30 seconds) and separates speech by speaker.

**What it does**:
- Uses pyannote.audio for speaker diarization (identifies different speakers)
- Segments audio into chunks of maximum 30 seconds
- Separates segments by speaker
- Saves segments to `output/segments/`

**Requirements**: HuggingFace API token for pyannote.audio model

**Usage**:
```bash
python utils/segment_audio.py
```

### 3. Audio Format Check (`check_mono.py`)

**Purpose**: Ensures all audio segments are in mono format for optimal ASR processing.

**What it does**:
- Checks if WAV files in `output/segments/` are mono
- Converts stereo files to mono by averaging channels
- Ensures consistent audio format for transcription

**Usage**:
```bash
python utils/check_mono.py
```

### 4. Transcription (`transcribe.py`)

**Purpose**: Transcribes audio segments using multiple ASR models for comparison.

**What it does**:
- Processes audio segments from `output/segments/`
- Uses multiple Whisper models and other ASR systems
- Handles timeouts gracefully (60-second limit per file)
- Saves transcripts to model-specific folders in `output/transcripts/`
- Tracks timeout information in `output/timeout_files.json`

**Usage**:
```bash
python utils/transcribe.py
```

**Note**: Modify the `model_list` in the script to use different ASR models.

### 5. Reference Transcript Processing (`process_gold_transcripts.py`)

**Purpose**: Processes gold standard reference transcripts for evaluation.

**What it does**:
- Reads original transcripts from `data/reference_transcripts/orthographic/`
- Creates cleaned versions (removes fillers like "uh", "eh", "ehm", "oh")
- Creates normalized versions (removes punctuation, lowercase)
- Saves processed versions to respective subdirectories

**Usage**:
```bash
python utils/process_gold_transcripts.py
```

### 6. Word Error Rate Evaluation (`wer_evaluator.py`)

**Purpose**: Evaluates ASR model performance using Word Error Rate (WER).

**What it does**:
- Compares ASR outputs against reference transcripts
- Calculates WER for each model
- Provides detailed evaluation metrics
- Handles different transcript formats and preprocessing

**Usage**:
```bash
python utils/wer_evaluator.py
```

### 7. Statistics and Counting (`counters.py`)

**Purpose**: Provides utility functions for counting words and calculating audio duration.

**What it does**:
- Counts total words across transcript files
- Calculates total audio duration
- Useful for dataset analysis and reporting

**Usage**:
```python
from utils.counters import count_total_words, get_total_audio_duration

# Count words in transcripts
word_count = count_total_words("output/transcripts/whisper-large-v2")

# Calculate audio duration
duration = get_total_audio_duration("output/segments")
```

## 📋 Complete Workflow

Here's the typical workflow for processing audio files:

1. **Prepare Data**:
   ```bash
   # Place audio files in data/raw/
   # Convert to WAV format
   python utils/convert_m4a_to_wav.py
   ```

2. **Segment Audio**:
   ```bash
   # Split into segments and separate by speaker
   python utils/segment_audio.py
   ```

3. **Check Audio Format**:
   ```bash
   # Ensure mono format
   python utils/check_mono.py
   ```

4. **Transcribe**:
   ```bash
   # Run transcription with multiple models
   python utils/transcribe.py
   ```

5. **Process Reference Transcripts** (if available):
   ```bash
   # Clean and normalize reference transcripts
   python utils/process_gold_transcripts.py
   ```

6. **Evaluate Performance** (if reference transcripts available):
   ```bash
   # Calculate WER scores
   python utils/wer_evaluator.py
   ```

## 🔑 Configuration

### API Keys
- **HuggingFace**: Required for pyannote.audio speaker diarization
- Store in `.secrets/hf_api_key.txt`

### Model Configuration
- Modify `model_list` in `transcribe.py` to use different ASR models
- Supported models include various Whisper variants and other ASR systems

## 📊 Output Structure

- **Segments**: `output/segments/` - Audio chunks (max 30s, separated by speaker)
- **Transcripts**: `output/transcripts/[model_name]/` - ASR outputs per model
- **Evaluation**: WER scores and timeout information
- **Reference**: Processed gold standard transcripts for evaluation

## 🛠️ Dependencies

Core dependencies (see `requirements.txt`):
- `pyannote.audio` - Speaker diarization
- `pydub` - Audio processing
- `librosa` - Audio analysis
- `soundfile` - Audio I/O
- `transformers` - ASR models
- `jiwer` - Word Error Rate calculation

## 📝 Notes

- The first run of segmentation will prompt you to log in to HuggingFace
- Transcription has a 60-second timeout per file to prevent hanging
- Supported audio formats: `wav`, `mp3`, `flac`, `ogg`, `m4a`
- The system is optimized for Dutch speech recognition
- Speaker diarization assumes 2 speakers by default (modifiable in code) 