"""
Flask application for audio file upload and waveform display
Week 17/11/25 Milestone
Enhanced with feature extraction - Week 24/11/25 Milestone
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import librosa
import numpy as np
from feature_extractor import AudioFeatureExtractor
import uuid

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
FEATURES_FOLDER = 'features'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FEATURES_FOLDER'] = FEATURES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FEATURES_FOLDER, exist_ok=True)

# Initialize feature extractor
feature_extractor = AudioFeatureExtractor()


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
    Handle audio file upload, return waveform data, and extract features

    Week 24/11/25: Enhanced with feature extraction

    Returns:
        JSON with audio metadata, waveform samples, and feature extraction status
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
        # Generate unique file ID to avoid conflicts
        file_id = str(uuid.uuid4())[:8]
        original_filename = secure_filename(file.filename)
        filename_base, filename_ext = os.path.splitext(original_filename)
        filename = f"{filename_base}_{file_id}{filename_ext}"

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

        # ===== Week 24/11/25: Extract and save features =====
        features, extraction_time = feature_extractor.extract_all_features(filepath)

        # Save features to JSON
        feature_filename = f"{filename_base}_{file_id}_features.json"
        feature_filepath = os.path.join(app.config['FEATURES_FOLDER'], feature_filename)
        feature_extractor.save_features(features, feature_filepath)

        # Prepare response
        response = {
            'file_id': file_id,
            'filename': original_filename,
            'duration': float(duration),
            'sample_rate': int(sr),
            'num_samples': len(y),
            'rms': rms,
            'waveform': waveform_samples,
            'features': {
                'extracted': True,
                'extraction_time': extraction_time,
                'feature_file': feature_filename,
                'mfcc_shape': features['mfcc']['shape'],
                'chroma_shape': features['chroma']['shape'],
                'tempo': features['audio_info']['tempo'],
                'num_beats': features['audio_info']['num_beats']
            },
            'message': 'File uploaded and features extracted successfully'
        }

        return jsonify(response), 200

    except Exception as e:
        # Clean up files if processing failed
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        if 'feature_filepath' in locals() and os.path.exists(feature_filepath):
            os.remove(feature_filepath)
        return jsonify({'error': f'Error processing audio file: {str(e)}'}), 500


@app.route('/api/features/<file_id>', methods=['GET'])
def get_features(file_id):
    """
    Retrieve extracted features for a specific file

    Week 24/11/25: New endpoint for feature retrieval

    Args:
        file_id: Unique file identifier

    Returns:
        JSON with extracted features or error if not found
    """
    try:
        # Find feature file matching the file_id
        feature_files = [f for f in os.listdir(app.config['FEATURES_FOLDER'])
                        if file_id in f and f.endswith('_features.json')]

        if not feature_files:
            return jsonify({
                'error': f'Features not found for file_id: {file_id}'
            }), 404

        # Load and return features
        feature_filepath = os.path.join(app.config['FEATURES_FOLDER'], feature_files[0])
        features = feature_extractor.load_features(feature_filepath)

        return jsonify({
            'file_id': file_id,
            'features': features,
            'message': 'Features retrieved successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': f'Error retrieving features: {str(e)}'}), 500


@app.route('/api/features', methods=['GET'])
def list_features():
    """
    List all available extracted features

    Week 24/11/25: Endpoint to list all feature files

    Returns:
        JSON with list of available feature files
    """
    try:
        feature_files = [f for f in os.listdir(app.config['FEATURES_FOLDER'])
                        if f.endswith('_features.json')]

        feature_list = []
        for feature_file in feature_files:
            feature_filepath = os.path.join(app.config['FEATURES_FOLDER'], feature_file)
            features = feature_extractor.load_features(feature_filepath)

            if features:
                feature_list.append({
                    'filename': feature_file,
                    'original_file': features['audio_info']['filename'],
                    'duration': features['audio_info']['duration'],
                    'extraction_time': features['extraction_time'],
                    'mfcc_shape': features['mfcc']['shape'],
                    'chroma_shape': features['chroma']['shape']
                })

        return jsonify({
            'count': len(feature_list),
            'features': feature_list,
            'message': f'Found {len(feature_list)} feature file(s)'
        }), 200

    except Exception as e:
        return jsonify({'error': f'Error listing features: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Audio upload service with feature extraction is running'
    }), 200


if __name__ == '__main__':
    print("Starting Flask server for audio upload and waveform display...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Allowed file types: {', '.join(ALLOWED_EXTENSIONS)}")
    app.run(debug=True, host='0.0.0.0', port=5000)
