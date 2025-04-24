import wave
import struct

def create_wav_file(output_file, sample_rate=44100):
    # Create a new WAV file
    with wave.open(output_file, 'wb') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        
        # Read the MP3 file as binary
        with open('text_to_speech.mp3', 'rb') as mp3:
            data = mp3.read()
        
        # Skip MP3 header (look for sync word 0xFFF)
        start = data.find(b'\xff\xfb')
        if start >= 0:
            data = data[start:]
        
        # Convert to 16-bit samples
        samples = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                # Convert each pair of bytes to a 16-bit sample
                sample = struct.unpack('h', data[i:i+2])[0]
                samples.append(sample)
        
        # Write the samples
        wav.writeframes(struct.pack('h' * len(samples), *samples))

if __name__ == "__main__":
    try:
        print("Converting MP3 to WAV...")
        create_wav_file('text_to_speech.wav')
        print("Conversion completed!")
    except Exception as e:
        print(f"Error during conversion: {e}") 