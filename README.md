# Audio Steganography Web Application

This Flask application provides a web interface for embedding and extracting hidden messages in WAV audio files using steganography techniques.

## Features

- Embed text messages in WAV audio files
- Extract hidden messages from WAV audio files
- Password protection for message security
- Support for various audio file formats (WAV)

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Embedding a Message

1. Navigate to the home page
2. Select a WAV audio file
3. Enter your message
4. Provide a password
5. Click "Embed Message"
6. Download the modified audio file

### Extracting a Message

1. Navigate to the home page
2. Select a WAV audio file containing a hidden message
3. Enter the password used during embedding
4. Click "Extract Message"
5. View the extracted message

## Security Notes

- Always use strong passwords to protect your hidden messages
- The original audio file is not modified; a new file is created
- Messages are encrypted using the provided password

## Technical Details

- Maximum file size: 16MB
- Supported audio format: WAV
- Message embedding uses LSB (Least Significant Bit) steganography
- Password verification ensures message integrity

## File Structure

```
.
├── src/
│   ├── __init__.py       # Package initialization
│   ├── main.py          # Main application entry point
│   ├── audio_handler.py # Audio file operations
│   ├── encryption.py    # Message encryption/decryption
│   ├── stego.py        # Steganography implementation
│   └── utils.py        # Logging and utilities
├── tests/
│   └── test_steganography.py  # Test suite
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── run_tests.py        # Test runner
└── README.md           # This file
```

## Logs

Logs are stored in the `results` directory with timestamps for debugging and monitoring.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

Feel free to submit issues and enhancement requests! 