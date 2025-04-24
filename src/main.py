import argparse
import logging
import os
import sys
sys.path.append(os.path.dirname(__file__))
from audio_handler import AudioHandler
from encryption import Encryptor
from stego import Steganography
from utils import setup_logging

def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Parse arguments
    parser = argparse.ArgumentParser(description='Audio Steganography Tool')
    parser.add_argument('--mode', choices=['embed', 'extract'], required=True,
                       help='Operation mode')
    parser.add_argument('--audio', required=True,
                       help='Input audio file path')
    parser.add_argument('--output', required=True,
                       help='Output file path')
    parser.add_argument('--message', help='Message file to hide')
    parser.add_argument('--password', required=True,
                       help='Encryption password')
    parser.add_argument('--lsb-depth', type=int, choices=range(1, 5),
                       default=2, help='LSB depth (1-4)')
    parser.add_argument('--key', help='Optional embedding key')

    args = parser.parse_args()

    try:
        audio_handler = AudioHandler()
        encryptor = Encryptor()
        stego = Steganography()

        if args.mode == 'embed':
            # Read and prepare data
            audio_data, sample_width, sample_rate = audio_handler.read_audio(args.audio)
            
            with open(args.message, 'rb') as f:
                message_data = f.read()

            # Calculate capacity
            capacity = audio_handler.get_capacity(audio_data, args.lsb_depth)
            logger.info(f"Available capacity: {capacity} bytes")
            
            # Encrypt message
            encrypted_data = encryptor.encrypt(message_data, args.password)
            
            if len(encrypted_data) > capacity:
                raise ValueError("Message too large for audio file")

            # Embed data
            stego_audio = stego.embed_data(audio_data, encrypted_data, 
                                         args.lsb_depth, args.key)
            
            # Save result
            audio_handler.save_audio(args.output, stego_audio, 
                                   sample_width, sample_rate)
            logger.info("Data embedded successfully")

        else:  # Extract mode
            # Read stego audio
            stego_audio, _, _ = audio_handler.read_audio(args.audio)
            
            # Extract encrypted data
            encrypted_data = stego.extract_data(stego_audio, 
                                              len(stego_audio) * args.lsb_depth // 8,
                                              args.lsb_depth, args.key)
            
            # Decrypt data
            decrypted_data = encryptor.decrypt(encrypted_data, args.password)
            
            # Save extracted data
            with open(args.output, 'wb') as f:
                f.write(decrypted_data)
            logger.info("Data extracted successfully")

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())