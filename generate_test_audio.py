import numpy as np
import wave

# Generate a 5-second sine wave at 440 Hz
duration = 5
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)

# Save as WAV file
with wave.open('test_audio.wav', 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    wav.writeframes(audio_data.tobytes()) 