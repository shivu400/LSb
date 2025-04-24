import subprocess
import os

def convert_mp3_to_wav(input_mp3, output_wav):
    try:
        # Using ffmpeg to convert MP3 to WAV with specific parameters
        command = [
            'ffmpeg',
            '-i', input_mp3,        # Input file
            '-acodec', 'pcm_s16le', # 16-bit PCM encoding
            '-ac', '1',             # Mono audio
            '-ar', '44100',         # 44.1kHz sample rate
            '-y',                   # Overwrite output file if exists
            output_wav
        ]
        
        print(f"Converting {input_mp3} to {output_wav}...")
        subprocess.run(command, check=True, capture_output=True)
        print("Conversion successful!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        print(f"ffmpeg error output: {e.stderr.decode()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_file = "text_to_speech.mp3"
    output_file = "text_to_speech.wav"
    convert_mp3_to_wav(input_file, output_file) 