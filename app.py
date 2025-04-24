from flask import Flask, render_template, request, jsonify, send_file
import os
import wave
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def embed_message(audio_path, message, password, lsb_depth):
    try:
        # Read the audio file
        with wave.open(audio_path, 'rb') as wav:
            params = wav.getparams()
            frames = wav.readframes(wav.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)

        # Convert message to binary
        message = password + ":" + message  # Add password to the message
        binary_message = ''.join(format(ord(c), '08b') for c in message) + '0' * 8  # Add null terminator

        if len(binary_message) > len(audio_data) * lsb_depth:
            return False, "Message too long for the audio file"

        # Embed the message
        binary_message_pos = 0
        modified_audio = audio_data.copy()

        for i in range(len(binary_message)):
            if binary_message_pos >= len(binary_message):
                break

            # Clear the LSBs and embed the message bits
            for j in range(lsb_depth):
                if binary_message_pos < len(binary_message):
                    bit = int(binary_message[binary_message_pos])
                    modified_audio[i] = (modified_audio[i] & ~(1 << j)) | (bit << j)
                    binary_message_pos += 1

        # Save the modified audio
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'embedded_' + os.path.basename(audio_path))
        with wave.open(output_path, 'wb') as wav:
            wav.setparams(params)
            wav.writeframes(modified_audio.tobytes())

        return True, output_path
    except Exception as e:
        return False, str(e)

def extract_message(audio_path, password, lsb_depth):
    try:
        # Read the audio file
        with wave.open(audio_path, 'rb') as wav:
            frames = wav.readframes(wav.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)

        # Extract binary message
        binary_message = ""
        for i in range(len(audio_data)):
            for j in range(lsb_depth):
                binary_message += str(audio_data[i] & (1 << j) and 1 or 0)

        # Convert binary to text
        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == "00000000":  # Null terminator
                break
            message += chr(int(byte, 2))

        # Verify password and extract message
        if ':' not in message:
            return False, "No hidden message found"

        stored_password, hidden_message = message.split(':', 1)
        if stored_password != password:
            return False, "Invalid password"

        return True, hidden_message
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hide')
def hide_message():
    return render_template('hide_message.html')

@app.route('/extract')
def extract_message_page():
    return render_template('extract_message.html')

@app.route('/embed', methods=['POST'])
def embed():
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'})

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'})

        if not allowed_file(audio_file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Only WAV files are allowed'})

        message = request.form.get('message', '')
        password = request.form.get('password', '')
        lsb_depth = int(request.form.get('lsb_depth', 1))

        if not message or not password:
            return jsonify({'success': False, 'error': 'Message and password are required'})

        filename = secure_filename(audio_file.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(audio_path)

        success, result = embed_message(audio_path, message, password, lsb_depth)
        
        if not success:
            return jsonify({'success': False, 'error': result})

        return jsonify({
            'success': True,
            'message': 'Message embedded successfully',
            'download_url': f'/download/{os.path.basename(result)}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/extract', methods=['POST'])
def extract():
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'})

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'})

        if not allowed_file(audio_file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Only WAV files are allowed'})

        password = request.form.get('password', '')
        lsb_depth = int(request.form.get('lsb_depth', 1))

        if not password:
            return jsonify({'success': False, 'error': 'Password is required'})

        filename = secure_filename(audio_file.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(audio_path)

        success, result = extract_message(audio_path, password, lsb_depth)
        
        if not success:
            return jsonify({'success': False, 'error': result})

        return jsonify({
            'success': True,
            'message': result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        as_attachment=True
    )

@app.after_request
def after_request(response):
    """Ensure proper CORS and caching headers"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True) 