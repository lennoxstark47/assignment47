"""
Test script for similarity calculation
Week 1/12/25 Milestone

Tests DTW and Cosine similarity with audio feature files
"""

import os
import sys
import json
import numpy as np
from similarity_calculator import SimilarityCalculator, compare_features
from feature_extractor import AudioFeatureExtractor
import librosa
import soundfile as sf


def create_test_audio_files():
    """
    Create synthetic test audio files with different similarity levels

    Returns:
        List of tuples (filename, description)
    """
    print("Creating test audio files...")

    # Create experiments folder if it doesn't exist
    os.makedirs('experiments', exist_ok=True)

    test_files = []

    # Create a simple sine wave (440 Hz - A note)
    sr = 22050
    duration = 3.0
    t = np.linspace(0, duration, int(sr * duration))

    # File 1: Pure 440 Hz sine wave (A note)
    y1 = 0.5 * np.sin(2 * np.pi * 440 * t)
    filename1 = 'experiments/test_audio_440hz.wav'
    sf.write(filename1, y1, sr)
    test_files.append((filename1, "440 Hz sine wave (A note)"))

    # File 2: Similar - 440 Hz with slight variation
    y2 = 0.5 * np.sin(2 * np.pi * 440 * t) * (1 + 0.1 * np.sin(2 * np.pi * 2 * t))
    filename2 = 'experiments/test_audio_440hz_variation.wav'
    sf.write(filename2, y2, sr)
    test_files.append((filename2, "440 Hz with modulation (similar to file 1)"))

    # File 3: Different frequency - 550 Hz (C# note)
    y3 = 0.5 * np.sin(2 * np.pi * 550 * t)
    filename3 = 'experiments/test_audio_550hz.wav'
    sf.write(filename3, y3, sr)
    test_files.append((filename3, "550 Hz sine wave (C# note - different)"))

    # File 4: Complex tone - chord with multiple frequencies
    y4 = (0.3 * np.sin(2 * np.pi * 440 * t) +
          0.3 * np.sin(2 * np.pi * 554 * t) +
          0.3 * np.sin(2 * np.pi * 659 * t))
    filename4 = 'experiments/test_audio_chord.wav'
    sf.write(filename4, y4, sr)
    test_files.append((filename4, "A major chord (440, 554, 659 Hz)"))

    print(f"Created {len(test_files)} test audio files")
    return test_files


def extract_features_for_test_files(test_files):
    """
    Extract features for all test files

    Args:
        test_files: List of (filename, description) tuples

    Returns:
        List of feature file paths
    """
    print("\nExtracting features for test files...")

    extractor = AudioFeatureExtractor()
    feature_files = []

    for filename, description in test_files:
        print(f"  - {description}")

        # Extract features
        features, extraction_time = extractor.extract_all_features(filename)

        # Save features
        base_name = os.path.splitext(os.path.basename(filename))[0]
        feature_filename = f'features/{base_name}_features.json'
        extractor.save_features(features, feature_filename)

        feature_files.append(feature_filename)
        print(f"    Extracted in {extraction_time:.3f}s -> {feature_filename}")

    return feature_files


def test_similarity_calculations(feature_files, test_files):
    """
    Test similarity calculations between different audio file pairs

    Args:
        feature_files: List of feature file paths
        test_files: List of (filename, description) tuples
    """
    print("\n" + "=" * 70)
    print("SIMILARITY CALCULATION TESTS")
    print("=" * 70)

    calculator = SimilarityCalculator()

    # Test pairs with expected similarity levels
    test_pairs = [
        (0, 1, "SIMILAR"),    # 440 Hz vs 440 Hz with variation
        (0, 2, "DIFFERENT"),  # 440 Hz vs 550 Hz
        (0, 3, "MODERATE"),   # 440 Hz vs chord containing 440 Hz
        (1, 2, "DIFFERENT"),  # 440 Hz variation vs 550 Hz
        (2, 3, "MODERATE"),   # 550 Hz vs chord
    ]

    results = []

    for idx1, idx2, expected in test_pairs:
        file1_desc = test_files[idx1][1]
        file2_desc = test_files[idx2][1]

        print(f"\nTest: {file1_desc}")
        print(f"  vs: {file2_desc}")
        print(f"  Expected: {expected} similarity")
        print("-" * 70)

        # Compare features
        comparison = compare_features(feature_files[idx1], feature_files[idx2])

        # Display results
        print(f"  Overall Similarity: {comparison['overall_similarity']:.2f}%")
        print(f"  Similarity Level: {comparison['similarity_level']}")
        print(f"\n  MFCC Comparison (Timbre/Texture):")
        print(f"    - DTW Distance: {comparison['mfcc_comparison']['dtw_distance']:.4f}")
        print(f"    - Cosine Similarity: {comparison['mfcc_comparison']['cosine_similarity']:.4f}")
        print(f"    - Euclidean Distance: {comparison['mfcc_comparison']['euclidean_distance']:.4f}")
        print(f"\n  Chroma Comparison (Harmony/Melody):")
        print(f"    - DTW Distance: {comparison['chroma_comparison']['dtw_distance']:.4f}")
        print(f"    - Cosine Similarity: {comparison['chroma_comparison']['cosine_similarity']:.4f}")
        print(f"    - Euclidean Distance: {comparison['chroma_comparison']['euclidean_distance']:.4f}")

        results.append({
            'pair': f"{os.path.basename(test_files[idx1][0])} vs {os.path.basename(test_files[idx2][0])}",
            'expected': expected,
            'overall_similarity': comparison['overall_similarity'],
            'similarity_level': comparison['similarity_level']
        })

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for result in results:
        print(f"{result['pair']}")
        print(f"  Expected: {result['expected']:10s} | "
              f"Got: {result['similarity_level']:15s} ({result['overall_similarity']:.2f}%)")


def test_existing_features():
    """
    Test with existing feature files if available
    """
    features_dir = 'features'

    if not os.path.exists(features_dir):
        print("No features directory found")
        return

    feature_files = [f for f in os.listdir(features_dir) if f.endswith('_features.json')]

    if len(feature_files) < 2:
        print("Need at least 2 feature files to compare")
        return

    print(f"\nFound {len(feature_files)} existing feature files:")
    for i, f in enumerate(feature_files[:5]):  # Show first 5
        print(f"  {i+1}. {f}")

    if len(feature_files) >= 2:
        print(f"\nComparing first two files as example...")
        file1 = os.path.join(features_dir, feature_files[0])
        file2 = os.path.join(features_dir, feature_files[1])

        comparison = compare_features(file1, file2)
        print(f"\nComparison Results:")
        print(f"  Overall Similarity: {comparison['overall_similarity']:.2f}%")
        print(f"  Similarity Level: {comparison['similarity_level']}")


def main():
    """
    Main test function
    """
    print("=" * 70)
    print("SIMILARITY CALCULATOR TEST SUITE")
    print("Week 1/12/25 Milestone")
    print("=" * 70)

    # Create features directory if it doesn't exist
    os.makedirs('features', exist_ok=True)

    # Create test audio files
    test_files = create_test_audio_files()

    # Extract features
    feature_files = extract_features_for_test_files(test_files)

    # Run similarity tests
    test_similarity_calculations(feature_files, test_files)

    # Test with existing features if available
    print("\n" + "=" * 70)
    print("Testing with existing uploaded features (if any):")
    print("=" * 70)
    test_existing_features()

    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)


if __name__ == '__main__':
    # Change to backend directory if not already there
    if os.path.basename(os.getcwd()) != 'backend':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)

    main()
