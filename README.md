# Audio Similarity Detection - Week 1

**Milestone:** Set up development environment; experiment with Web Audio API/Librosa
**Week:** 10/11/25
**Status:** ✅ Completed

## What Was Done This Week

This week focused on setting up the development environment and conducting initial experiments with both server-side (Librosa) and client-side (Web Audio API) audio processing approaches.

## Files Created

### Backend (Python + Librosa)
```
backend/
├── requirements.txt                    # Python dependencies
└── experiments/
    ├── librosa_experiment.py          # Librosa feature extraction demo
    ├── test_audio.wav                 # Generated test audio (5 seconds)
    ├── librosa_features.png           # Feature visualizations
    └── librosa_results.json           # Extraction results
```

### Frontend (Web Audio API)
```
web_audio_experiment.html              # Simple Web Audio API test
```

### Documentation
```
TECH_STACK_EVALUATION.md               # Technology comparison
INSTRUCTIONS.md                         # Project timeline & workflow
```

## How to Run Experiments

### Librosa Experiment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run experiment
python experiments/librosa_experiment.py
```

**Output:**
- Generates test audio file
- Extracts MFCC, chromagram, spectral features
- Creates visualization PNG
- Saves results to JSON

### Web Audio API Experiment

```bash
# Simply open in browser
open web_audio_experiment.html
# Or: python3 -m http.server 8000
# Then visit: http://localhost:8000/web_audio_experiment.html
```

**Features:**
- Upload audio file
- Display basic features (duration, sample rate, RMS, ZCR)
- Draw waveform visualization

## Key Findings

**Librosa (Server-side):**
- ✅ Provides MFCCs, chromagram, spectral features
- ✅ Processing time: ~22 seconds (can be optimized)
- ✅ Suitable for achieving 80%+ accuracy target

**Web Audio API (Client-side):**
- ✅ Fast processing (<1 second)
- ✅ Good for waveform visualization
- ❌ Missing MFCC and chromagram support
- ❌ Not suitable for main similarity detection

**Recommendation:** Use Librosa for backend processing, Web Audio API for frontend visualization only.

## Next Steps

**Week of 17/11/25:** Implement audio file upload and basic waveform display
- Create Flask application with upload endpoint
- Build basic frontend interface
- Integrate waveform visualization

---

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for full project timeline and workflow.
