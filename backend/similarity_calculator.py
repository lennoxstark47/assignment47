"""
Similarity Calculation Module
Week 1/12/25 Milestone

Implements DTW (Dynamic Time Warping) and Cosine Similarity algorithms
for comparing audio feature vectors.
"""

import numpy as np
from typing import Dict, Tuple, Optional
import json
import os
from scipy.spatial.distance import cosine as scipy_cosine
from scipy.spatial.distance import euclidean


class SimilarityCalculator:
    """
    Calculate similarity between audio features using various algorithms
    """

    def __init__(self):
        """Initialize similarity calculator"""
        pass

    def dtw_distance(self, seq1: np.ndarray, seq2: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Calculate Dynamic Time Warping (DTW) distance between two sequences

        DTW is a dynamic programming algorithm that finds the optimal alignment
        between two time series sequences. It's particularly useful for comparing
        audio features that may have different tempos or slight timing variations.

        Args:
            seq1: First sequence (n_features x time_frames_1)
            seq2: Second sequence (n_features x time_frames_2)

        Returns:
            Tuple of (dtw_distance, cost_matrix)
        """
        # Ensure sequences are 2D arrays
        if seq1.ndim == 1:
            seq1 = seq1.reshape(-1, 1)
        if seq2.ndim == 1:
            seq2 = seq2.reshape(-1, 1)

        # Transpose if features are in rows instead of columns
        if seq1.shape[0] < seq1.shape[1]:
            seq1 = seq1.T
        if seq2.shape[0] < seq2.shape[1]:
            seq2 = seq2.T

        n, m = len(seq1), len(seq2)

        # Initialize cost matrix with infinity
        dtw_matrix = np.full((n + 1, m + 1), np.inf)
        dtw_matrix[0, 0] = 0

        # Fill the DTW matrix using dynamic programming
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Calculate Euclidean distance between frames
                cost = euclidean(seq1[i - 1], seq2[j - 1])

                # Take minimum of three possible paths
                dtw_matrix[i, j] = cost + min(
                    dtw_matrix[i - 1, j],      # insertion
                    dtw_matrix[i, j - 1],      # deletion
                    dtw_matrix[i - 1, j - 1]   # match
                )

        # The DTW distance is in the bottom-right corner
        dtw_distance = dtw_matrix[n, m]

        # Normalize by the sum of sequence lengths to make it comparable
        normalized_distance = dtw_distance / (n + m)

        return normalized_distance, dtw_matrix

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors

        Cosine similarity measures the cosine of the angle between two vectors,
        ranging from -1 (opposite) to 1 (identical). It's useful for comparing
        the overall spectral characteristics of audio files.

        Args:
            vec1: First feature vector
            vec2: Second feature vector

        Returns:
            Cosine similarity score (0 to 1, where 1 is most similar)
        """
        # Flatten arrays if needed
        vec1 = np.array(vec1).flatten()
        vec2 = np.array(vec2).flatten()

        # Handle edge case where vectors have different lengths
        if len(vec1) != len(vec2):
            min_len = min(len(vec1), len(vec2))
            vec1 = vec1[:min_len]
            vec2 = vec2[:min_len]

        # Calculate cosine similarity (1 - cosine distance)
        # scipy's cosine returns distance, so we convert to similarity
        similarity = 1 - scipy_cosine(vec1, vec2)

        return float(similarity)

    def euclidean_distance(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate Euclidean distance between two vectors

        Args:
            vec1: First feature vector
            vec2: Second feature vector

        Returns:
            Euclidean distance (lower is more similar)
        """
        vec1 = np.array(vec1).flatten()
        vec2 = np.array(vec2).flatten()

        if len(vec1) != len(vec2):
            min_len = min(len(vec1), len(vec2))
            vec1 = vec1[:min_len]
            vec2 = vec2[:min_len]

        return float(euclidean(vec1, vec2))

    def compare_mfcc_features(self, features1: Dict, features2: Dict) -> Dict:
        """
        Compare MFCC features between two audio files

        Args:
            features1: First audio's features dictionary
            features2: Second audio's features dictionary

        Returns:
            Dictionary with comparison results
        """
        # Extract MFCC data
        mfcc1 = np.array(features1['mfcc']['mfcc'])
        mfcc2 = np.array(features2['mfcc']['mfcc'])

        # Extract MFCC statistics for cosine similarity
        mfcc1_mean = np.array(features1['mfcc']['mfcc_mean'])
        mfcc2_mean = np.array(features2['mfcc']['mfcc_mean'])

        # Calculate DTW distance on full MFCC sequences
        dtw_dist, _ = self.dtw_distance(mfcc1, mfcc2)

        # Calculate cosine similarity on MFCC means
        cosine_sim = self.cosine_similarity(mfcc1_mean, mfcc2_mean)

        # Calculate Euclidean distance on MFCC means
        euclidean_dist = self.euclidean_distance(mfcc1_mean, mfcc2_mean)

        return {
            'dtw_distance': float(dtw_dist),
            'cosine_similarity': float(cosine_sim),
            'euclidean_distance': float(euclidean_dist),
            'mfcc1_shape': features1['mfcc']['shape'],
            'mfcc2_shape': features2['mfcc']['shape']
        }

    def compare_chroma_features(self, features1: Dict, features2: Dict) -> Dict:
        """
        Compare Chroma features between two audio files

        Args:
            features1: First audio's features dictionary
            features2: Second audio's features dictionary

        Returns:
            Dictionary with comparison results
        """
        # Extract Chroma data
        chroma1 = np.array(features1['chroma']['chroma'])
        chroma2 = np.array(features2['chroma']['chroma'])

        # Extract Chroma statistics for cosine similarity
        chroma1_mean = np.array(features1['chroma']['chroma_mean'])
        chroma2_mean = np.array(features2['chroma']['chroma_mean'])

        # Calculate DTW distance on full Chroma sequences
        dtw_dist, _ = self.dtw_distance(chroma1, chroma2)

        # Calculate cosine similarity on Chroma means
        cosine_sim = self.cosine_similarity(chroma1_mean, chroma2_mean)

        # Calculate Euclidean distance on Chroma means
        euclidean_dist = self.euclidean_distance(chroma1_mean, chroma2_mean)

        return {
            'dtw_distance': float(dtw_dist),
            'cosine_similarity': float(cosine_sim),
            'euclidean_distance': float(euclidean_dist),
            'chroma1_shape': features1['chroma']['shape'],
            'chroma2_shape': features2['chroma']['shape']
        }

    def calculate_overall_similarity(self, features1: Dict, features2: Dict) -> Dict:
        """
        Calculate overall similarity between two audio files using multiple metrics

        Args:
            features1: First audio's features dictionary
            features2: Second audio's features dictionary

        Returns:
            Dictionary with comprehensive comparison results
        """
        # Compare MFCC features (timbre/texture similarity)
        mfcc_comparison = self.compare_mfcc_features(features1, features2)

        # Compare Chroma features (harmonic/melodic similarity)
        chroma_comparison = self.compare_chroma_features(features1, features2)

        # Calculate weighted overall similarity score (0-100%)
        # Higher weight on DTW cosine similarity for both features
        mfcc_score = (mfcc_comparison['cosine_similarity'] * 0.6 +
                     (1 - min(mfcc_comparison['dtw_distance'], 1.0)) * 0.4)

        chroma_score = (chroma_comparison['cosine_similarity'] * 0.6 +
                       (1 - min(chroma_comparison['dtw_distance'], 1.0)) * 0.4)

        # Combine MFCC and Chroma scores (MFCC weighted slightly higher)
        overall_similarity = (mfcc_score * 0.6 + chroma_score * 0.4) * 100

        # Determine similarity level
        if overall_similarity >= 80:
            similarity_level = "Very High"
        elif overall_similarity >= 60:
            similarity_level = "High"
        elif overall_similarity >= 40:
            similarity_level = "Moderate"
        elif overall_similarity >= 20:
            similarity_level = "Low"
        else:
            similarity_level = "Very Low"

        return {
            'overall_similarity': float(overall_similarity),
            'similarity_level': similarity_level,
            'mfcc_comparison': mfcc_comparison,
            'chroma_comparison': chroma_comparison,
            'audio1_info': features1['audio_info'],
            'audio2_info': features2['audio_info']
        }

    def compare_audio_files(self, feature_file1: str, feature_file2: str) -> Dict:
        """
        Compare two audio files by loading their pre-extracted features

        Args:
            feature_file1: Path to first feature JSON file
            feature_file2: Path to second feature JSON file

        Returns:
            Dictionary with comparison results
        """
        # Load features
        with open(feature_file1, 'r') as f:
            features1 = json.load(f)

        with open(feature_file2, 'r') as f:
            features2 = json.load(f)

        # Calculate similarity
        results = self.calculate_overall_similarity(features1, features2)

        return results


def compare_features(feature_file1: str, feature_file2: str) -> Dict:
    """
    Convenience function to compare two feature files

    Args:
        feature_file1: Path to first feature JSON file
        feature_file2: Path to second feature JSON file

    Returns:
        Comparison results dictionary
    """
    calculator = SimilarityCalculator()
    return calculator.compare_audio_files(feature_file1, feature_file2)


if __name__ == '__main__':
    """
    Test the similarity calculator with sample features
    """
    # This will be used for testing once we have feature files
    print("Similarity Calculator Module")
    print("=" * 50)
    print("\nImplemented algorithms:")
    print("  - Dynamic Time Warping (DTW)")
    print("  - Cosine Similarity")
    print("  - Euclidean Distance")
    print("\nFeature comparisons:")
    print("  - MFCC comparison (timbre/texture)")
    print("  - Chroma comparison (harmony/melody)")
    print("\nUse compare_features() to compare two audio files")
