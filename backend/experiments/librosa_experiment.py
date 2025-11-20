"""
Librosa Audio Processing Experiment
=====================================
This script demonstrates the capabilities of Librosa for audio feature extraction.
Features tested:
- MFCC (Mel-Frequency Cepstral Coefficients)
- Chromagram (pitch class energy)
- Spectral analysis
- Tempo estimation
"""

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
from pathlib import Path
import json
import time


class LibrosaExperiment:
    """Experiment class to test Librosa capabilities"""

    def __init__(self, sample_rate=22050):
        """
        Initialize the experiment

        Args:
            sample_rate: Target sample rate for audio processing
        """
        self.sample_rate = sample_rate
        self.results = {}

    def generate_test_audio(self, duration=5):
        """
        Generate a simple test audio signal (sine wave with harmonics)

        Args:
            duration: Length of audio in seconds

        Returns:
            y: Audio time series
            sr: Sample rate
        """
        print(f"\n[1/7] Generating test audio ({duration}s)...")

        # Generate a musical note (A4 = 440 Hz) with harmonics
        t = np.linspace(0, duration, int(self.sample_rate * duration))

        # Fundamental frequency (A4)
        fundamental = 440

        # Create a musical tone with harmonics
        y = (
            np.sin(2 * np.pi * fundamental * t) +           # Fundamental
            0.5 * np.sin(2 * np.pi * fundamental * 2 * t) + # 2nd harmonic
            0.25 * np.sin(2 * np.pi * fundamental * 3 * t)  # 3rd harmonic
        )

        # Normalize
        y = y / np.max(np.abs(y))

        # Save to file
        output_path = Path(__file__).parent / 'test_audio.wav'
        sf.write(output_path, y, self.sample_rate)

        print(f"✓ Test audio generated: {output_path}")
        print(f"  Duration: {duration}s, Sample rate: {self.sample_rate} Hz")

        return y, self.sample_rate

    def extract_mfcc(self, y, sr):
        """
        Extract MFCC features

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            mfccs: MFCC feature matrix
        """
        print("\n[2/7] Extracting MFCCs...")
        start_time = time.time()

        # Extract MFCCs (13 coefficients is standard)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        elapsed = time.time() - start_time

        print(f"✓ MFCCs extracted in {elapsed:.4f}s")
        print(f"  Shape: {mfccs.shape} (13 coefficients x {mfccs.shape[1]} frames)")
        print(f"  Mean: {np.mean(mfccs):.4f}, Std: {np.std(mfccs):.4f}")

        self.results['mfcc'] = {
            'shape': mfccs.shape,
            'extraction_time': elapsed,
            'mean': float(np.mean(mfccs)),
            'std': float(np.std(mfccs))
        }

        return mfccs

    def extract_chroma(self, y, sr):
        """
        Extract chromagram features

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            chroma: Chromagram feature matrix
        """
        print("\n[3/7] Extracting Chromagram...")
        start_time = time.time()

        # Extract chromagram
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)

        elapsed = time.time() - start_time

        print(f"✓ Chromagram extracted in {elapsed:.4f}s")
        print(f"  Shape: {chroma.shape} (12 pitch classes x {chroma.shape[1]} frames)")
        print(f"  Dominant pitch class: {np.argmax(np.mean(chroma, axis=1))}")

        self.results['chroma'] = {
            'shape': chroma.shape,
            'extraction_time': elapsed,
            'dominant_pitch_class': int(np.argmax(np.mean(chroma, axis=1)))
        }

        return chroma

    def extract_spectral_features(self, y, sr):
        """
        Extract spectral features

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            dict: Various spectral features
        """
        print("\n[4/7] Extracting Spectral Features...")
        start_time = time.time()

        # Spectral centroid (brightness)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]

        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]

        elapsed = time.time() - start_time

        print(f"✓ Spectral features extracted in {elapsed:.4f}s")
        print(f"  Spectral Centroid (mean): {np.mean(spectral_centroid):.2f} Hz")
        print(f"  Spectral Rolloff (mean): {np.mean(spectral_rolloff):.2f} Hz")
        print(f"  Zero Crossing Rate (mean): {np.mean(zcr):.6f}")

        self.results['spectral'] = {
            'extraction_time': elapsed,
            'spectral_centroid_mean': float(np.mean(spectral_centroid)),
            'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
            'zero_crossing_rate_mean': float(np.mean(zcr))
        }

        return {
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'zcr': zcr
        }

    def estimate_tempo(self, y, sr):
        """
        Estimate tempo

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            tempo: Estimated tempo in BPM
        """
        print("\n[5/7] Estimating Tempo...")
        start_time = time.time()

        # Estimate tempo
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]

        elapsed = time.time() - start_time

        print(f"✓ Tempo estimated in {elapsed:.4f}s")
        print(f"  Estimated tempo: {tempo:.2f} BPM")

        self.results['tempo'] = {
            'extraction_time': elapsed,
            'tempo_bpm': float(tempo)
        }

        return tempo

    def calculate_similarity(self, y1, y2, sr):
        """
        Calculate similarity between two audio signals using cosine similarity

        Args:
            y1: First audio time series
            y2: Second audio time series
            sr: Sample rate

        Returns:
            similarity: Similarity score (0-1)
        """
        print("\n[6/7] Calculating Similarity...")
        start_time = time.time()

        # Extract MFCCs for both signals
        mfcc1 = librosa.feature.mfcc(y=y1, sr=sr, n_mfcc=13)
        mfcc2 = librosa.feature.mfcc(y=y2, sr=sr, n_mfcc=13)

        # Ensure same length
        min_length = min(mfcc1.shape[1], mfcc2.shape[1])
        mfcc1 = mfcc1[:, :min_length]
        mfcc2 = mfcc2[:, :min_length]

        # Calculate cosine similarity
        from sklearn.metrics.pairwise import cosine_similarity

        # Flatten and reshape for cosine_similarity
        mfcc1_flat = mfcc1.flatten().reshape(1, -1)
        mfcc2_flat = mfcc2.flatten().reshape(1, -1)

        similarity = cosine_similarity(mfcc1_flat, mfcc2_flat)[0][0]

        elapsed = time.time() - start_time

        print(f"✓ Similarity calculated in {elapsed:.4f}s")
        print(f"  Cosine similarity: {similarity:.4f}")

        self.results['similarity'] = {
            'calculation_time': elapsed,
            'cosine_similarity': float(similarity)
        }

        return similarity

    def visualize_features(self, y, sr, mfccs, chroma):
        """
        Create visualizations of extracted features

        Args:
            y: Audio time series
            sr: Sample rate
            mfccs: MFCC features
            chroma: Chromagram features
        """
        print("\n[7/7] Creating Visualizations...")

        fig, axes = plt.subplots(4, 1, figsize=(12, 10))

        # Waveform
        librosa.display.waveshow(y, sr=sr, ax=axes[0])
        axes[0].set_title('Waveform')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('Amplitude')

        # MFCCs
        img1 = librosa.display.specshow(mfccs, sr=sr, x_axis='time', ax=axes[1])
        axes[1].set_title('MFCC')
        axes[1].set_ylabel('MFCC Coefficients')
        fig.colorbar(img1, ax=axes[1])

        # Chromagram
        img2 = librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma', ax=axes[2])
        axes[2].set_title('Chromagram')
        fig.colorbar(img2, ax=axes[2])

        # Spectrogram
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img3 = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', ax=axes[3])
        axes[3].set_title('Spectrogram')
        fig.colorbar(img3, ax=axes[3], format='%+2.0f dB')

        plt.tight_layout()

        # Save figure
        output_path = Path(__file__).parent / 'librosa_features.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')

        print(f"✓ Visualization saved: {output_path}")

        return output_path

    def save_results(self):
        """Save experiment results to JSON file"""
        output_path = Path(__file__).parent / 'librosa_results.json'

        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✓ Results saved: {output_path}")

        return output_path

    def run_full_experiment(self):
        """Run the complete experiment"""
        print("=" * 60)
        print("LIBROSA AUDIO PROCESSING EXPERIMENT")
        print("=" * 60)

        # Generate test audio
        y, sr = self.generate_test_audio(duration=5)

        # Extract features
        mfccs = self.extract_mfcc(y, sr)
        chroma = self.extract_chroma(y, sr)
        spectral_features = self.extract_spectral_features(y, sr)
        tempo = self.estimate_tempo(y, sr)

        # Test similarity (compare signal with itself)
        similarity = self.calculate_similarity(y, y, sr)

        # Create visualizations
        viz_path = self.visualize_features(y, sr, mfccs, chroma)

        # Save results
        results_path = self.save_results()

        print("\n" + "=" * 60)
        print("EXPERIMENT COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nTotal features extracted:")
        print(f"  - MFCCs: {mfccs.shape[0]} coefficients")
        print(f"  - Chromagram: {chroma.shape[0]} pitch classes")
        print(f"  - Spectral features: 3 types")
        print(f"  - Tempo: Estimated")
        print(f"\nTotal processing time: {sum([r['extraction_time'] if 'extraction_time' in r else r.get('calculation_time', 0) for r in self.results.values()]):.4f}s")

        return {
            'results': self.results,
            'visualization': str(viz_path),
            'results_file': str(results_path)
        }


def main():
    """Main function to run the experiment"""
    experiment = LibrosaExperiment()
    experiment.run_full_experiment()


if __name__ == '__main__':
    main()
