 import soundfile as sf
import numpy as np

def convert_to_wav(input_file, output_file):
    try:
        # Read the audio data
        print(f"Converting {input_file} to {output_file}...")
        data, samplerate = sf.read(input_file)
        
        # Ensure mono
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        
        # Convert to 16-bit PCM
        data = (data * 32767).astype(np.int16)
        
        # Write WAV file
        sf.write(output_file, data, samplerate, subtype='PCM_16')
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    input_file = "text_to_speech.mp3"
    output_file = "text_to_speech.wav"
    convert_to_wav(input_file, output_file) 