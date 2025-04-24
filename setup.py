from setuptools import setup, find_packages

setup(
    name="audio-steganography",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "wave>=0.0.2",
    ],
    entry_points={
        'console_scripts': [
            'audio-stego=src.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for hiding and extracting secret messages in WAV audio files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/audio-steganography",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 