import numpy as np
from typing import Tuple, Optional
import logging
import random

class Steganography:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_embedding_positions(self, data_length: int, audio_length: int, 
                                  key: Optional[str] = None) -> np.ndarray:
        """
        Generate embedding positions, optionally using a pseudo-random sequence
        """
        positions = np.arange(audio_length)
        if key:
            random.seed(key)
            random.shuffle(positions)
        return positions[:data_length]

    def embed_data(self, audio_data: np.ndarray, secret_data: bytes, 
                  lsb_depth: int, key: Optional[str] = None) -> np.ndarray:
        """
        Embed secret data into audio using enhanced LSB technique
        """
        try:
            # Convert secret data to bit array
            bit_array = np.unpackbits(np.frombuffer(secret_data, dtype=np.uint8))
            required_samples = len(bit_array) // lsb_depth
            
            if required_samples > len(audio_data):
                raise ValueError("Secret data too large for audio file")

            # Create copy of audio data
            stego_audio = audio_data.copy()
            
            # Generate embedding positions
            positions = self.generate_embedding_positions(required_samples, 
                                                       len(audio_data), key)

            # Embed data
            for i, pos in enumerate(positions):
                bit_start = i * lsb_depth
                bit_end = bit_start + lsb_depth
                sample_bits = bit_array[bit_start:bit_end]
                
                # Clear LSBs and embed new bits
                stego_audio[pos] = (stego_audio[pos] >> lsb_depth << lsb_depth) | \
                                 int(''.join(map(str, sample_bits)), 2)

            return stego_audio
        except Exception as e:
            self.logger.error(f"Embedding error: {e}")
            raise

    def extract_data(self, stego_audio: np.ndarray, data_length: int, 
                    lsb_depth: int, key: Optional[str] = None) -> bytes:
        """
        Extract hidden data from stego audio
        """
        try:
            required_samples = (data_length * 8 + lsb_depth - 1) // lsb_depth
            
            # Generate extraction positions
            positions = self.generate_embedding_positions(required_samples, 
                                                       len(stego_audio), key)

            # Extract bits
            extracted_bits = []
            for pos in positions:
                sample = stego_audio[pos]
                bits = [int(b) for b in format(sample & ((1 << lsb_depth) - 1), 
                       f'0{lsb_depth}b')]
                extracted_bits.extend(bits)

            # Convert bits to bytes
            extracted_bits = np.array(extracted_bits[:data_length * 8])
            extracted_bytes = np.packbits(extracted_bits)
            
            return bytes(extracted_bytes)
        except Exception as e:
            self.logger.error(f"Extraction error: {e}")
            raise