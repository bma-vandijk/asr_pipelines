#!/usr/bin/env python3
"""
Transcript cleaning module for removing capitalisation, punctuation, 
leading/trailing whitespace, and fillers from transcript files.
This module only READS from the original transcripts and creates a new
cleaned folder structure without modifying the original files.
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Set


class TranscriptCleaner:
    """Clean transcripts by removing various elements."""
    
    def __init__(self):
        # Common Dutch fillers, hesitations, and unknown words
        self.fillers = {
            'uh', 'um', 'hè', 'huh', 'hm', 'hmm', 'eh', 'euh', 'uhm', 'oh', 'ehm'
            }
        
        # Punctuation to remove
        self.punctuation = r'[.,!?;:()\[\]{}"\'-]'
        
    def clean_text(self, text: str) -> str:
        """
        Clean a single text string by removing:
        - Capitalisation
        - Punctuation
        - Leading/trailing whitespace
        - Fillers and hesitations
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text string
        """
        # Remove unknown tokens (independent, sentence boundaries, or embedded)
        text = re.sub(r'\[UNK\]', '', text)
        
        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = re.sub(self.punctuation, '', text)
        
        # Remove leading and trailing whitespace
        text = text.strip()
        
        # Split into words
        words = text.split()
        
        # Remove fillers
        cleaned_words = []
        for word in words:
            # Skip if it's a filler
            if word not in self.fillers:
                cleaned_words.append(word)
        
        # Join words back together
        cleaned_text = ' '.join(cleaned_words)
        
        # Remove extra whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        return cleaned_text.strip()
    
    def process_file(self, input_path: str, output_path: str) -> None:
        """
        Process a single transcript file.
        
        Args:
            input_path: Path to input transcript file (READ ONLY)
            output_path: Path to output cleaned transcript file (NEW FILE)
        """
        try:
            # Read from original file (READ ONLY)
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Clean the content
            cleaned_content = self.clean_text(content)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write cleaned content to NEW file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
                
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
    
    def process_directory(self, input_dir: str, output_dir: str) -> None:
        """
        Process all transcript files in a directory and its subdirectories.
        Creates a completely new folder structure for cleaned transcripts.
        
        Args:
            input_dir: Input directory containing transcript files (READ ONLY)
            output_dir: Output directory for cleaned transcripts (NEW FOLDER)
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        # Check if input directory exists
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory '{input_dir}' does not exist")
        
        # Remove output directory if it exists (to ensure clean start)
        if output_path.exists():
            print(f"Removing existing output directory: {output_dir}")
            shutil.rmtree(output_path)
        
        # Create fresh output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all .txt files in input directory and subdirectories
        txt_files = list(input_path.rglob('*.txt'))
        
        print(f"Found {len(txt_files)} transcript files to process")
        print(f"Reading from: {input_dir}")
        print(f"Writing cleaned files to: {output_dir}")
        
        processed_count = 0
        for txt_file in txt_files:
            # Calculate relative path from input directory
            relative_path = txt_file.relative_to(input_path)
            
            # Create corresponding output path
            output_file = output_path / relative_path
            
            # Process the file (READ from original, WRITE to new location)
            self.process_file(str(txt_file), str(output_file))
            processed_count += 1
            
            if processed_count % 100 == 0:
                print(f"Processed {processed_count} files...")
        
        print(f"Completed processing {processed_count} files")
        print(f"Cleaned transcripts saved to: {output_dir}")
        print("Original transcripts remain unchanged.")


def main():
    """Main function to run the transcript cleaning process."""
    # Define paths
    input_dir = os.path.join("output", "transcripts")
    output_dir = os.path.join("output", "transcripts_cleaned")
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    # Create cleaner instance
    cleaner = TranscriptCleaner()
    
    # Process all transcripts
    cleaner.process_directory(input_dir, output_dir)


if __name__ == "__main__":
    main() 