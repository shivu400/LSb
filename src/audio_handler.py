import wave
import numpy as np
from typing import Tuple, Union
import logging

class AudioHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_audio(self, audio_path: str) -> Tuple[np.ndarray, int, int]:
        """
        Read WAV audio file and return samples, sample width, and sample rate
        """
        try:
            with wave.open(audio_path, 'rb') as wav:
                params = wav.getparams()
                frames = wav.readframes(params.nframes)
                audio_data = np.frombuffer(frames, dtype=np.int16)
                return audio_data, params.sampwidth, params.framerate
        except Exception as e:
            self.logger.error(f"Error reading audio file: {e}")
            raise

    def save_audio(self, audio_path: str, audio_data: np.ndarray, 
                   sample_width: int, sample_rate: int) -> None:
        """
        Save modified audio data to WAV file
        """
        try:
            with wave.open(audio_path, 'wb') as wav:
                wav.setnchannels(1)  # Mono audio
                wav.setsampwidth(sample_width)
                wav.setframerate(sample_rate)
                wav.writeframes(audio_data.tobytes())
        except Exception as e:
            self.logger.error(f"Error saving audio file: {e}")
            raise

    def get_capacity(self, audio_data: np.ndarray, lsb_depth: int) -> int:
        """
        Calculate maximum capacity in bytes for given LSB depth
        """
        return len(audio_data) * lsb_depth // 8