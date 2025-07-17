"""
Word Error Rate (WER) Evaluator for ASR Systems

This module provides functions to evaluate the performance of ASR systems
by calculating Word Error Rate between reference and hypothesis transcripts.
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Tuple
import jiwer


def read_reference_transcripts(ref_path: str = "data/reference_transcripts/normalized") -> List[str]:
    """
    Read reference transcripts from the specified folder.
    
    Args:
        ref_path: Path to folder containing reference transcript files
        
    Returns:
        List of reference transcript strings, sorted by filename
    """
    ref_files = sorted(glob.glob(os.path.join(ref_path, "*.txt")))
    transcripts = []
    
    for file_path in ref_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            transcript = f.read().strip()
            transcripts.append(transcript)
    
    return transcripts


def read_asr_transcripts(asr_path: str = "output/transcripts") -> Dict[str, List[str]]:
    """
    Read ASR transcripts from subfolders containing different model outputs.
    
    Args:
        asr_path: Path to folder containing subfolders with ASR model transcripts
        
    Returns:
        Dictionary mapping model names to lists of transcript strings
    """
    model_transcripts = {}
    
    # Get all subdirectories (model folders)
    model_dirs = [d for d in os.listdir(asr_path) 
                  if os.path.isdir(os.path.join(asr_path, d)) and not d.startswith('.')]
    
    for model_dir in model_dirs:
        model_path = os.path.join(asr_path, model_dir)
        transcript_files = sorted(glob.glob(os.path.join(model_path, "*.txt")))
        
        transcripts = []
        for file_path in transcript_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                transcript = f.read().strip()
                transcripts.append(transcript)
        
        model_transcripts[model_dir] = transcripts
    
    return model_transcripts


def calculate_wer(reference: str, hypothesis: str) -> float:
    """
    Calculate Word Error Rate between reference and hypothesis.
    
    Args:
        reference: Reference transcript string
        hypothesis: Hypothesis transcript string
        
    Returns:
        WER as a float (0.0 = perfect, higher = more errors)
    """
    return jiwer.wer(reference, hypothesis)


def evaluate_wer(ref_transcripts: List[str], model_transcripts: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Evaluate WER for all models against reference transcripts.
    
    Args:
        ref_transcripts: List of reference transcript strings
        model_transcripts: Dictionary mapping model names to transcript lists
        
    Returns:
        Dictionary mapping model names to average WER scores
    """
    results = {}
    
    for model_name, hyp_transcripts in model_transcripts.items():
        if len(hyp_transcripts) != len(ref_transcripts):
            print(f"Warning: Mismatch in transcript counts for {model_name}")
            continue
            
        total_wer = 0.0
        valid_pairs = 0
        
        for ref, hyp in zip(ref_transcripts, hyp_transcripts):
            if ref.strip() and hyp.strip():  # Skip empty transcripts
                wer = calculate_wer(ref, hyp)
                total_wer += wer
                valid_pairs += 1
        
        avg_wer = total_wer / valid_pairs if valid_pairs > 0 else float('inf')
        results[model_name] = avg_wer
    
    return results
