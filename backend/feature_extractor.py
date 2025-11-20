"""
Feature Extraction Module
Week 24/11/25 Milestone

Extracts audio features (MFCC and Chroma) for similarity detection
"""

import librosa
import numpy as np
import json
import os
from typing import Dict, Tuple, Optional
import time


class AudioFeatureExtractor:
    """
    Extract MFCC and Chroma features from audio files
    """

    def __init__(self):
        """Initialize feature extractor with default parameters"""
        # MFCC parameters
        self.n_mfcc = 13  # Standard number of MFCC coefficients
        self.n_fft = 2048  # FFT window size
        self.hop_length = 512  # Number of samples between frames

        # Chroma parameters
        self.n_chroma = 12  # 12 pitch classes (C, C#, D, ..., B)

    def extract_mfcc(self, y: np.ndarray, sr: int) -> Dict:
        """
        Extract MFCC (Mel-Frequency Cepstral Coefficients) features

        MFCCs represent the short-term power spectrum of a sound and are
        commonly used in audio recognition and music similarity tasks.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Dictionary containing MFCC data and statistics
        """
        # Extract MFCC features
        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )

        # Calculate statistics for each MFCC coefficient
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)
        mfcc_min = np.min(mfcc, axis=1)
        mfcc_max = np.max(mfcc, axis=1)

        return {
            'mfcc': mfcc.tolist(),  # Full MFCC matrix (n_mfcc x time_frames)
            'mfcc_mean': mfcc_mean.tolist(),
            'mfcc_std': mfcc_std.tolist(),
            'mfcc_min': mfcc_min.tolist(),
            'mfcc_max': mfcc_max.tolist(),
            'shape': mfcc.shape,  # (n_mfcc, time_frames)
            'n_mfcc': self.n_mfcc,
            'n_fft': self.n_fft,
            'hop_length': self.hop_length
        }

    def extract_chroma(self, y: np.ndarray, sr: int) -> Dict:
        """
        Extract Chroma features (pitch class profiles)

        Chroma features capture harmonic and melodic characteristics
        by representing the intensity of the 12 pitch classes.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Dictionary containing Chroma data and statistics
        """
        # Extract Chroma features
        chroma = librosa.feature.chroma_stft(
            y=y,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_chroma=self.n_chroma
        )

        # Calculate statistics for each pitch class
        chroma_mean = np.mean(chroma, axis=1)
        chroma_std = np.std(chroma, axis=1)
        chroma_min = np.min(chroma, axis=1)
        chroma_max = np.max(chroma, axis=1)

        return {
            'chroma': chroma.tolist(),  # Full Chroma matrix (12 x time_frames)
            'chroma_mean': chroma_mean.tolist(),
            'chroma_std': chroma_std.tolist(),
            'chroma_min': chroma_min.tolist(),
            'chroma_max': chroma_max.tolist(),
            'shape': chroma.shape,  # (12, time_frames)
            'n_chroma': self.n_chroma,
            'pitch_classes': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        }

    def extract_all_features(self, filepath: str) -> Tuple[Dict, float]:
        """
        Extract all features from an audio file

        Args:
            filepath: Path to audio file

        Returns:
            Tuple of (features dictionary, extraction time in seconds)
        """
        start_time = time.time()

        # Load audio file
        y, sr = librosa.load(filepath, sr=None, mono=True)

        # Extract features
        mfcc_features = self.extract_mfcc(y, sr)
        chroma_features = self.extract_chroma(y, sr)

        # Get basic audio info
        duration = librosa.get_duration(y=y, sr=sr)

        # Calculate tempo and beat frames
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        extraction_time = time.time() - start_time

        # Combine all features
        features = {
            'audio_info': {
                'filename': os.path.basename(filepath),
                'duration': float(duration),
                'sample_rate': int(sr),
                'num_samples': len(y),
                'tempo': float(tempo),
                'num_beats': len(beat_frames)
            },
            'mfcc': mfcc_features,
            'chroma': chroma_features,
            'extraction_time': extraction_time
        }

        return features, extraction_time

    def save_features(self, features: Dict, output_path: str) -> None:
        """
        Save extracted features to JSON file

        Args:
            features: Features dictionary
            output_path: Path to save JSON file
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(features, f, indent=2)

    def load_features(self, filepath: str) -> Optional[Dict]:
        """
        Load previously extracted features from JSON file

        Args:
            filepath: Path to JSON file

        Returns:
            Features dictionary or None if file doesn't exist
        """
        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            return json.load(f)


def extract_and_save_features(audio_path: str, output_dir: str = 'features') -> Dict:
    """
    Convenience function to extract and save features in one step

    Args:
        audio_path: Path to audio file
        output_dir: Directory to save features

    Returns:
        Extracted features dictionary
    """
    extractor = AudioFeatureExtractor()
    features, extraction_time = extractor.extract_all_features(audio_path)

    # Create output filename based on audio filename
    audio_filename = os.path.basename(audio_path)
    feature_filename = os.path.splitext(audio_filename)[0] + '_features.json'
    output_path = os.path.join(output_dir, feature_filename)

    extractor.save_features(features, output_path)

    print(f"Features extracted in {extraction_time:.2f}s")
    print(f"Saved to: {output_path}")

    return features


if __name__ == '__main__':
    """
    Test the feature extractor with sample audio
    """
    # Test with the experiment audio file
    test_audio = 'experiments/test_audio.wav'

    if os.path.exists(test_audio):
        print("Testing feature extraction...")
        features = extract_and_save_features(test_audio, output_dir='features')

        print("\n=== Extraction Summary ===")
        print(f"Duration: {features['audio_info']['duration']:.2f}s")
        print(f"Sample Rate: {features['audio_info']['sample_rate']} Hz")
        print(f"Tempo: {features['audio_info']['tempo']:.1f} BPM")
        print(f"MFCC shape: {features['mfcc']['shape']}")
        print(f"Chroma shape: {features['chroma']['shape']}")
        print(f"Extraction time: {features['extraction_time']:.2f}s")
    else:
        print(f"Test audio file not found: {test_audio}")
