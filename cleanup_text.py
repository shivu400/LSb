def cleanup_text(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # Extract only the actual message (before any binary data)
        clean_text = text.split('\x00')[0]  # Split at first null byte
        
        # Further cleanup: keep only the actual message
        if 'Testing LSB steganography' in clean_text:
            clean_text = clean_text[:clean_text.find('Testing LSB steganography') + len('Testing LSB steganography with depth 2.')]
        
        # Remove any remaining non-printable characters
        clean_text = ''.join(char for char in clean_text if char.isprintable() or char.isspace())
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(clean_text.strip())
        
        print(f"Cleaned text saved to {output_file}")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_text("extracted_saripoda.txt", "clean_message.txt") 