import os
import unittest
import numpy as np
from src.audio_handler import AudioHandler
from src.encryption import Encryptor
from src.stego import Steganography

class TestSteganography(unittest.TestCase):
    def setUp(self):
        # Create test audio data
        self.sample_rate = 44100
        self.duration = 1
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        self.audio_data = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
        self.test_message = b"Hello, this is a test message!"
        self.password = "testpassword123"
        
        # Initialize components
        self.audio_handler = AudioHandler()
        self.encryptor = Encryptor()
        self.stego = Steganography()

    def test_encryption_decryption(self):
        """Test that encryption and decryption work correctly"""
        encrypted = self.encryptor.encrypt(self.test_message, self.password)
        decrypted = self.encryptor.decrypt(encrypted, self.password)
        self.assertEqual(self.test_message, decrypted)

    def test_embedding_extraction(self):
        """Test the complete embedding and extraction process"""
        # Calculate capacity
        capacity = self.audio_handler.get_capacity(self.audio_data, lsb_depth=2)
        self.assertGreater(capacity, len(self.test_message))

        # Encrypt and embed
        encrypted = self.encryptor.encrypt(self.test_message, self.password)
        stego_audio = self.stego.embed_data(self.audio_data, encrypted, lsb_depth=2)

        # Extract and decrypt
        extracted_encrypted = self.stego.extract_data(stego_audio, len(encrypted), lsb_depth=2)
        extracted_message = self.encryptor.decrypt(extracted_encrypted, self.password)

        self.assertEqual(self.test_message, extracted_message)

    def test_audio_integrity(self):
        """Test that the audio data remains mostly unchanged"""
        encrypted = self.encryptor.encrypt(self.test_message, self.password)
        stego_audio = self.stego.embed_data(self.audio_data, encrypted, lsb_depth=2)

        # Check that the audio data is similar but not identical
        self.assertTrue(np.any(self.audio_data != stego_audio))
        # Check that the changes are small (within LSB range)
        diff = np.abs(self.audio_data - stego_audio)
        self.assertTrue(np.all(diff <= 3))  # For 2-bit LSB, max difference is 3

if __name__ == '__main__':
    unittest.main() 