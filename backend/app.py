"""
Flask application for audio file upload and waveform display
Week 17/11/25 Milestone
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import librosa
import numpy as np

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle audio file upload and return waveform data

    Returns:
        JSON with audio metadata and waveform samples
    """
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({
            'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400

    try:
        # Save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load audio file with librosa
        y, sr = librosa.load(filepath, sr=None, mono=True)

        # Get audio metadata
        duration = librosa.get_duration(y=y, sr=sr)

        # Downsample waveform for visualization (max 1000 points)
        # This makes it efficient to send to frontend
        target_samples = min(1000, len(y))
        if len(y) > target_samples:
            # Use linear interpolation to downsample
            indices = np.linspace(0, len(y) - 1, target_samples, dtype=int)
            waveform_samples = y[indices].tolist()
        else:
            waveform_samples = y.tolist()

        # Calculate RMS energy for display
        rms = float(np.sqrt(np.mean(y**2)))

        # Prepare response
        response = {
            'filename': filename,
            'duration': float(duration),
            'sample_rate': int(sr),
            'num_samples': len(y),
            'rms': rms,
            'waveform': waveform_samples,
            'message': 'File uploaded successfully'
        }

        return jsonify(response), 200

    except Exception as e:
        # Clean up file if processing failed
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'Error processing audio file: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Audio upload service is running'
    }), 200


if __name__ == '__main__':
    print("Starting Flask server for audio upload and waveform display...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    app.run(debug=True, host='0.0.0.0', port=5000)
