from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class Encryptor:
    def __init__(self):
        self.salt_length = 16
        self.iv_length = 16
        self.key_length = 32  # for AES-256
        self.iterations = 100000  # for PBKDF2

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        return PBKDF2(
            password.encode(), 
            salt, 
            dkLen=self.key_length,
            count=self.iterations
        )

    def encrypt(self, data: bytes, password: str) -> bytes:
        """
        Encrypt data using AES-256-CBC with PBKDF2 key derivation.
        Format: salt + iv + encrypted_data
        """
        try:
            # Generate random salt and IV
            salt = get_random_bytes(self.salt_length)
            iv = get_random_bytes(self.iv_length)

            # Derive key from password
            key = self._derive_key(password, salt)

            # Create cipher and encrypt data
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_data = cipher.encrypt(pad(data, AES.block_size))

            # Combine salt + iv + encrypted_data
            return salt + iv + encrypted_data

        except Exception as e:
            raise ValueError(f"Encryption error: {str(e)}")

    def decrypt(self, encrypted_data: bytes, password: str) -> bytes:
        """
        Decrypt AES-256-CBC encrypted data using password.
        Format: salt + iv + encrypted_data
        """
        try:
            # Extract salt, iv, and encrypted data
            salt = encrypted_data[:self.salt_length]
            iv = encrypted_data[self.salt_length:self.salt_length + self.iv_length]
            data = encrypted_data[self.salt_length + self.iv_length:]

            # Derive key from password and salt
            key = self._derive_key(password, salt)

            # Create cipher and decrypt data
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(data), AES.block_size)

            return decrypted_data

        except Exception as e:
            raise ValueError(f"Decryption error: {str(e)}")
