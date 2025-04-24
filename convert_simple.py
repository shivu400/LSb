import wave
import numpy as np

# Read the raw bytes
with open('saripoda.wav.WAV', 'rb') as f:
    data = f.read()

# Try to find audio data by looking for common patterns
# Remove any headers that might be causing issues
data = data[data.find(b'\xff\xfb'):]  # Look for MP3 frame sync

# Create a simple WAV file
with wave.open('saripoda_converted.wav', 'wb') as wav:
    wav.setnchannels(1)  # Mono
    wav.setsampwidth(2)  # 16-bit
    wav.setframerate(44100)  # Standard sample rate
    wav.writeframes(data)

print("Conversion attempt completed") 