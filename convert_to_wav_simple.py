from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import os

def convert_to_wav(input_file, output_file):
    try:
        # Load MP3 and convert to WAV
        print(f"Converting {input_file} to {output_file}...")
        
        # First convert using pydub
        audio = AudioSegment.from_mp3(input_file)
        
        # Convert to mono and set parameters
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(44100)
        audio = audio.set_sample_width(2)  # 16-bit
        
        # Export as WAV
        audio.export(output_file, format='wav')
        print("Conversion successful!")
        
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    input_file = "text_to_speech.mp3"
    output_file = "text_to_speech.wav"
    convert_to_wav(input_file, output_file) 