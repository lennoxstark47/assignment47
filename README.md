# Audio Similarity Detection System

**Project:** Web-Based Music Plagiarism Detection
**Duration:** September 2025 - May 2026
**Current Status:** Week 8/12/25 - Comparison Visualization Interface ✅

## Project Overview

A web application for detecting melodic and rhythmic similarities between music tracks to assist in plagiarism identification. Uses advanced audio processing techniques (Librosa) with an intuitive web interface.

## Current Progress

### ✅ Completed Milestones

**Week 10/11/25: Development Environment Setup**
- Python backend with Librosa
- Web Audio API experiments
- Technology stack evaluation
- [View Details](TECH_STACK_EVALUATION.md)

**Week 17/11/25: Audio Upload & Waveform Display**
- Flask RESTful API with upload endpoint
- Interactive web interface with drag-and-drop
- Real-time waveform visualization
- Audio metadata extraction
- [View Details](WEEK_17_11_25.md)

**Week 24/11/25: Feature Extraction Module**
- MFCC and Chroma feature extraction
- Automatic feature extraction on upload
- Feature storage and retrieval API
- Performance testing (0.029s avg extraction time)
- [View Details](WEEK_24_11_25.md)

**Week 1/12/25: Similarity Calculation Algorithm**
- DTW (Dynamic Time Warping) implementation
- Cosine similarity calculation
- Comparison API endpoint (`POST /api/compare`)
- Comprehensive test suite with synthetic audio
- [View Details](WEEK_01_12_25.md)

**Week 8/12/25: Comparison Visualization Interface**
- Dual file upload interface with drag-and-drop
- Side-by-side waveform comparison display
- Overall similarity score with visual indicator
- Detailed MFCC and Chroma metrics display
- Responsive, modern UI with gradient design
- [View Details](WEEK_08_12_25.md)

## Project Structure

```
assignment47/
├── backend/
│   ├── app.py                          # Flask application
│   ├── feature_extractor.py            # Feature extraction module
│   ├── similarity_calculator.py        # Similarity calculation module (NEW)
│   ├── test_upload.py                  # Upload test script
│   ├── test_features.py                # Feature extraction tests
│   ├── test_similarity.py              # Similarity calculation tests (NEW)
│   ├── requirements.txt                # Python dependencies
│   ├── features/                       # Extracted features storage
│   └── experiments/
│       ├── librosa_experiment.py       # Feature extraction demo
│       ├── test_audio.wav              # Test audio (5 seconds)
│       ├── librosa_features.png        # Feature visualizations
│       └── librosa_results.json        # Extraction results
│
├── frontend/
│   └── index.html                      # Web interface
│
├── web_audio_experiment.html           # Web Audio API experiment
├── INSTRUCTIONS.md                     # Project timeline & workflow
├── TECH_STACK_EVALUATION.md            # Technology comparison
├── WEEK_17_11_25.md                    # Week 2 milestone docs
├── WEEK_24_11_25.md                    # Week 3 milestone docs
├── WEEK_01_12_25.md                    # Week 4 milestone docs
├── WEEK_08_12_25.md                    # Week 5 milestone docs (NEW)
└── README.md                           # This file
```

## Quick Start

### Running the Application

1. **Set up backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start Flask server:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   - Open browser to `http://localhost:5000`
   - Upload an audio file (MP3, WAV, OGG, FLAC, M4A)
   - View waveform visualization and metadata

### Running Experiments

**Librosa Experiment:**
```bash
cd backend
source venv/bin/activate
python experiments/librosa_experiment.py
```

**Web Audio API Experiment:**
```bash
# Open web_audio_experiment.html in browser
python3 -m http.server 8000
# Visit: http://localhost:8000/web_audio_experiment.html
```

## Current Features

### Audio Upload & Processing
- ✅ Drag-and-drop file upload interface
- ✅ Support for multiple audio formats (MP3, WAV, OGG, FLAC, M4A)
- ✅ File validation (type and size checks, max 10MB)
- ✅ Real-time processing feedback

### Waveform Visualization
- ✅ HTML5 Canvas-based waveform display
- ✅ Efficient data downsampling (1000 points)
- ✅ Responsive design
- ✅ Audio metadata display (duration, sample rate, RMS energy)

### Backend API
- ✅ RESTful upload endpoint (`POST /api/upload`)
- ✅ Feature extraction endpoints (`GET /api/features`, `GET /api/features/<file_id>`)
- ✅ Comparison endpoint (`POST /api/compare`)
- ✅ Health check endpoint (`GET /api/health`)
- ✅ Librosa-based audio processing
- ✅ MFCC and Chroma feature extraction
- ✅ DTW and Cosine similarity algorithms
- ✅ Automated testing suite

## Technology Stack

**Backend:**
- Python 3.8+
- Flask (Web framework)
- Librosa (Audio processing)
- NumPy, SciPy (Scientific computing)

**Frontend:**
- HTML5, CSS3, JavaScript
- Canvas API (Waveform visualization)
- Responsive design (no frameworks yet)

**Audio Features:**
- ✅ MFCC extraction (13 coefficients)
- ✅ Chroma features (12 pitch classes)
- ✅ Tempo and beat detection
- ✅ Feature storage and retrieval

**Similarity Calculation:**
- ✅ Dynamic Time Warping (DTW) algorithm
- ✅ Cosine similarity calculation
- ✅ Euclidean distance metrics
- ✅ Overall similarity scoring (0-100%)
- ✅ Similarity level classification

**Comparison Visualization:**
- ✅ Dual file upload interface
- ✅ Side-by-side waveform display
- ✅ Overall similarity score visualization
- ✅ Detailed MFCC and Chroma metrics

## Next Milestone

**Week 15/12/25: Test Dataset Compilation**
- Compile test dataset of audio files
- Begin initial accuracy testing
- Document testing methodology
- Collect baseline performance metrics

## Documentation

- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Full project timeline & workflow
- [TECH_STACK_EVALUATION.md](TECH_STACK_EVALUATION.md) - Technology comparison
- [WEEK_17_11_25.md](WEEK_17_11_25.md) - Week 2 milestone documentation
- [WEEK_24_11_25.md](WEEK_24_11_25.md) - Week 3 milestone documentation
- [WEEK_01_12_25.md](WEEK_01_12_25.md) - Week 4 milestone documentation
- [WEEK_08_12_25.md](WEEK_08_12_25.md) - Week 5 milestone documentation
- [claude.md](claude.md) - Project reference guide

## Testing

**Upload Tests:**
```bash
cd backend
source venv/bin/activate
python test_upload.py
```

**Feature Extraction Tests:**
```bash
cd backend
source venv/bin/activate
python test_features.py
```

**Similarity Calculation Tests:**
```bash
cd backend
source venv/bin/activate
python test_similarity.py
```

## Project Goals

- 80%+ accuracy on plagiarism detection
- Processing time < 30 seconds per comparison
- User-friendly web interface
- Comprehensive testing with 15-20 participants
- 6,000-word technical report

**Project Timeline:** 22/9/25 - 4/5/26 (32 weeks)
**Current Phase:** Week 5 of 32 - Implementation phase
