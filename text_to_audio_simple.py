from gtts import gTTS
import os

def text_to_audio(text_file, output_file):
    try:
        # Read the text file
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        # Convert text to speech
        print("Converting text to speech...")
        tts = gTTS(text=text, lang='en')
        
        # Save directly as MP3
        tts.save(output_file)
        print(f"Successfully created {output_file}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    input_file = "clean_message.txt"
    output_file = "text_to_speech.mp3"  # Using MP3 format directly
    text_to_audio(input_file, output_file) 