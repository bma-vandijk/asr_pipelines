import os
import torch
import gc
import signal
import json
from datetime import datetime
from transformers import pipeline

SEGMENTS_DIR = os.path.join('output', 'segments')
TRANSCRIPT_TIMEOUT = 60 # seconds
OUTPUT_DIR = 'output'
OUTPUT_TRANSCRIPT_DIR = os.path.join('output', 'transcripts')

os.makedirs(OUTPUT_TRANSCRIPT_DIR, exist_ok=True)
os.environ["PATH"] += os.pathsep + os.path.join("opt", "homebrew", "bin")

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Transcription took too long")

def transcribe_segments(model_list, cpu=True):
    # Dictionary to store timeout information
    timeout_info = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'timeouts': {}
    }
    
    for model_name in model_list:
        transcriber = pipeline("automatic-speech-recognition", model=model_name, device="cpu" if cpu else "mps")
        model_output_dir = os.path.join(OUTPUT_TRANSCRIPT_DIR, model_name.split('/')[-1])
        os.makedirs(model_output_dir, exist_ok=True)
        
        # Initialize timeout list for this model
        timeout_info['timeouts'][model_name] = []

        for filename in os.listdir(SEGMENTS_DIR):
            if filename.lower().endswith(('.wav', '.mp3', '.flac', '.ogg', '.m4a')):
                # Check if transcription already exists
                output_path = os.path.join(model_output_dir, f"{os.path.splitext(filename)[0]}.txt")
                if os.path.exists(output_path):
                    #print(f"Skipping {filename} - already transcribed with {model_name}")
                    continue

                #print("Currently transcribing: ", filename)
                audio_path = os.path.join(SEGMENTS_DIR, filename)
                
                # Set timeout for 60 seconds
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(TRANSCRIPT_TIMEOUT)
                
                try:
                    result = transcriber(audio_path, generate_kwargs={"language": "nl"})
                    transcription = result["text"]
                    with open(output_path, 'w') as f:
                        f.write(transcription)
                    print(f"Transcribed {filename} using {model_name}")
                except TimeoutError:
                    print(f"Timeout while transcribing {filename} - moving to next file")
                    timeout_info['timeouts'][model_name].append(filename)
                    # Create a file with 'None' for timeout cases
                    with open(output_path, 'w') as f:
                        f.write('None')
                    continue
                finally:
                    signal.alarm(0)  # Disable the alarm

        #Clear cache/memory after each model
        del transcriber
        gc.collect()
        torch.mps.empty_cache() if torch.backends.mps.is_available() else None

    # Save timeout information
    timeout_file = os.path.join(OUTPUT_DIR, 'timeout_files.json')
    with open(timeout_file, 'w') as f:
        json.dump(timeout_info, f, indent=4)
    
    # Print summary of timeouts
    print("\nTimeout Summary:")
    print("===============")
    for model, files in timeout_info['timeouts'].items():
        if files:
            print(f"\nModel: {model}")
            print("Files that timed out:")
            for file in files:
                print(f"- {file}") 