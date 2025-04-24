import numpy as np
import wave
from scipy.io import wavfile
import soundfile as sf

def convert_to_wav(input_file, output_file):
    try:
        # First try using soundfile which supports multiple formats
        print("Attempting to read with soundfile...")
        data, sample_rate = sf.read(input_file)
        
        # Convert to mono if stereo
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        
        # Normalize and convert to 16-bit PCM
        data = np.int16(data * 32767)
        
        # Save as WAV
        with wave.open(output_file, 'wb') as wav:
            wav.setnchannels(1)  # Mono
            wav.setsampwidth(2)  # 16-bit
            wav.setframerate(sample_rate)
            wav.writeframes(data.tobytes())
        print(f"Successfully converted to {output_file}")
        
    except Exception as e:
        print(f"Error with soundfile: {e}")
        try:
            # Try with scipy as fallback
            print("Attempting to read with scipy.io.wavfile...")
            sample_rate, data = wavfile.read(input_file)
            
            # Convert to mono if stereo
            if len(data.shape) > 1:
                data = data.mean(axis=1).astype(np.int16)
            
            # Save as WAV
            with wave.open(output_file, 'wb') as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(sample_rate)
                wav.writeframes(data.tobytes())
            print(f"Successfully converted to {output_file}")
            
        except Exception as e:
            print(f"Error with scipy: {e}")
            print("Conversion failed. The input file might be corrupted or in an unsupported format.") 