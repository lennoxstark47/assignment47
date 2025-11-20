# Project Reference: Web-Based Audio Similarity Detection System

## Project Overview
This is an undergraduate project focused on developing a web application for music plagiarism analysis through audio similarity detection.

## Research Question
How effectively can web-based audio processing technologies detect melodic and rhythmic similarities between music tracks to assist in plagiarism identification?

## Core Requirements

### Functional Requirements
- Accept two audio file uploads (MP3/WAV format, up to 5 minutes)
- Extract audio features using signal processing techniques
- Calculate similarity scores between tracks
- Display results within 30 seconds of upload
- Achieve 80%+ accuracy in detecting intentionally similar test cases

### Technical Implementation

#### Technology Stack
**Frontend:**
- HTML5, CSS3, JavaScript
- Web Audio API for client-side audio processing
- Visualization: D3.js or Chart.js

**Backend (Alternative):**
- Python Flask
- Librosa for server-side audio analysis

#### Audio Processing Techniques
- **Feature Extraction:**
  - Short-Time Fourier Transform (STFT)
  - Mel-Frequency Cepstral Coefficients (MFCCs)
  - Chromagram analysis
  - Tempo analysis

- **Similarity Algorithms:**
  - Cosine similarity
  - Cross-correlation
  - Dynamic Time Warping (DTW)

### User Interface Features
- Audio file upload interface
- Comparative waveform visualizations
- Similarity percentage score with confidence metrics
- Highlighted sections showing similar melodic/rhythmic patterns
- Intuitive result display

## Testing & Validation

### Test Dataset Sources
- Royalty-free music libraries (Free Music Archive, YouTube Audio Library, ccMixter)
- Public domain classical music variations
- Academic datasets (GTZAN, Million Song Dataset subsets)
- Published musicology plagiarism case examples

### User Testing
- 15-20 participants (music students, hobbyist musicians, general users)
- Likert scale questionnaire for usability and accuracy evaluation
- Comparison of system assessments vs. human musical judgment

### Evaluation Metrics
- Confusion matrices (true/false positives)
- ROC curves for threshold optimization
- Accuracy percentage against ground truth
- Qualitative user feedback analysis

## Project Timeline
**Duration:** 22/9/25 - 4/5/26 (32 weeks)

**Key Milestones:**
- Week of 20/10/25: Ethics form completion, literature search begins
- Week of 10/11/25: Development environment setup, Web Audio API experiments
- Week of 17/11/25: Audio upload and waveform display implementation
- Week of 24/11/25: Feature extraction module development
- Week of 1/12/25: Similarity calculation algorithm implementation
- Week of 8/12/25: Comparison visualization interface
- Week of 15/12/25: Test dataset compilation, initial testing
- Week of 9/2/26: User testing begins (2 weeks)
- Week of 23/3/26: Project Showcase
- 30/4/26: Final report submission (6,000 words)
- Week of 4/5/26: Demonstration with supervisor

## Deliverables
1. Fully functional web application
2. 6,000-word technical report (design, implementation, testing, evaluation)
3. Source code repository with documentation
4. User testing results and analysis
5. Face-to-face demonstration

## Ethical Considerations
- Informed consent from all user testing participants
- Anonymized participant responses
- Minimal demographic data collection (musical background only)
- Only royalty-free/public domain/self-created audio files for testing
- Full ethics application following university guidelines
- GDPR compliance for data storage
- Participant withdrawal rights

## Required Resources

### Software (All Free)
- VS Code
- Web Audio API / Python with Librosa/NumPy
- D3.js or Chart.js
- GitHub (student account)

### Hardware
- Personal laptop with adequate processing power
- Headphones for audio testing

### Data
- Free Music Archive, YouTube Audio Library, ccMixter
- GTZAN Genre Collection

### Human Resources
- 15-20 volunteer participants (social media/university recruitment)

## Background Context
- Addresses gaps in accessible music plagiarism detection
- Inspired by high-profile cases ("Blurred Lines", Ed Sheeran disputes)
- Current solutions: expensive forensic musicology or proprietary systems
- Challenge: subjective nature of musical similarity (melody, rhythm, harmony, structure)
- Combines web development, DSP, algorithm design, and UX

## Success Criteria
- System achieves 80%+ accuracy on test cases
- Processes audio files within 30-second timeframe
- Positive user feedback on usability
- Clear visual representation of similarity results
- Documented limitations and future improvements
