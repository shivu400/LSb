from scipy.io import wavfile
import numpy as np

# Create a 5-second test audio file
sample_rate = 44100
duration = 5
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = np.sin(2 * np.pi * 440 * t) * 32767
audio_data = audio_data.astype(np.int16)

# Save as WAV
wavfile.write('d:\\LSB\\input.wav', sample_rate, audio_data)