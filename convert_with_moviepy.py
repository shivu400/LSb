from moviepy.editor import AudioFileClip

def convert_to_wav(input_file, output_file):
    try:
        print(f"Converting {input_file} to {output_file}...")
        audio = AudioFileClip(input_file)
        audio.write_audiofile(output_file, fps=44100, nbytes=2, codec='pcm_s16le')
        audio.close()
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    input_file = "text_to_speech.mp3"
    output_file = "text_to_speech.wav"
    convert_to_wav(input_file, output_file) 