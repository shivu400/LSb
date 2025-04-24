import numpy as np
import wave

# Generate a 10-second audio with multiple frequencies
duration = 10
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration))

# Create a more complex waveform (combination of frequencies)
frequencies = [440, 880, 1320]  # A4, A5, E6 notes
audio_data = np.zeros_like(t)
for freq in frequencies:
    audio_data += np.sin(2 * np.pi * freq * t)

# Normalize and convert to 16-bit integer
audio_data = (audio_data * 32767 / len(frequencies)).astype(np.int16)

# Save as WAV file
with wave.open('test_complex.wav', 'wb') as wav:
    wav.setnchannels(1)  # Mono
    wav.setsampwidth(2)  # 2 bytes per sample
    wav.setframerate(sample_rate)
    wav.writeframes(audio_data.tobytes()) 