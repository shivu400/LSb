import numpy as np
import wave
from gtts import gTTS
import os
from pydub import AudioSegment

def text_to_wav(text_file, output_wav):
    try:
        # Read the text file
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        # First convert text to speech using gTTS (Google Text-to-Speech)
        print("Converting text to speech...")
        tts = gTTS(text=text, lang='en')
        
        # Save as temporary MP3
        temp_mp3 = "temp_speech.mp3"
        tts.save(temp_mp3)
        
        # Convert MP3 to WAV using pydub
        print("Converting to WAV format...")
        audio = AudioSegment.from_mp3(temp_mp3)
        
        # Convert to mono and set sample width to 16-bit
        audio = audio.set_channels(1)
        audio = audio.set_sample_width(2)
        
        # Export as WAV
        audio.export(output_wav, format="wav")
        
        # Clean up temporary file
        os.remove(temp_mp3)
        
        print(f"Successfully created {output_wav}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    input_file = "clean_message.txt"
    output_file = "text_to_speech.wav"
    text_to_wav(input_file, output_file) 