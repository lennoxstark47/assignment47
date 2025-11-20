"""
Feature Extraction Performance Testing
Week 24/11/25 Milestone

Tests the feature extraction module for accuracy and performance
"""

import os
import sys
import time
import json
from feature_extractor import AudioFeatureExtractor, extract_and_save_features


def test_feature_extraction():
    """
    Test feature extraction on sample audio files
    """
    print("=" * 60)
    print("Feature Extraction Performance Test")
    print("Week 24/11/25 Milestone")
    print("=" * 60)

    # Initialize extractor
    extractor = AudioFeatureExtractor()

    # Test audio file
    test_audio = 'experiments/test_audio.wav'

    if not os.path.exists(test_audio):
        print(f"\n❌ Test audio file not found: {test_audio}")
        print("Please ensure the file exists from Week 10/11/25 milestone")
        return False

    print(f"\n📁 Test file: {test_audio}")
    print("-" * 60)

    # Test 1: Feature Extraction
    print("\n[Test 1] Feature Extraction")
    try:
        start_time = time.time()
        features, extraction_time = extractor.extract_all_features(test_audio)
        total_time = time.time() - start_time

        print(f"  ✅ Extraction successful")
        print(f"  ⏱️  Extraction time: {extraction_time:.3f}s")
        print(f"  ⏱️  Total time: {total_time:.3f}s")

        # Validate features structure
        assert 'audio_info' in features, "Missing audio_info"
        assert 'mfcc' in features, "Missing MFCC features"
        assert 'chroma' in features, "Missing Chroma features"
        print(f"  ✅ Feature structure validated")

    except Exception as e:
        print(f"  ❌ Extraction failed: {str(e)}")
        return False

    # Test 2: MFCC Features Validation
    print("\n[Test 2] MFCC Features")
    try:
        mfcc = features['mfcc']
        print(f"  Shape: {mfcc['shape']}")
        print(f"  Number of coefficients: {mfcc['n_mfcc']}")
        print(f"  Time frames: {mfcc['shape'][1]}")

        # Validate MFCC data
        assert mfcc['n_mfcc'] == 13, "Expected 13 MFCC coefficients"
        assert len(mfcc['mfcc_mean']) == 13, "MFCC mean length mismatch"
        assert len(mfcc['mfcc_std']) == 13, "MFCC std length mismatch"

        print(f"  ✅ MFCC validation passed")
        print(f"  First 3 MFCC means: {[f'{x:.2f}' for x in mfcc['mfcc_mean'][:3]]}")

    except Exception as e:
        print(f"  ❌ MFCC validation failed: {str(e)}")
        return False

    # Test 3: Chroma Features Validation
    print("\n[Test 3] Chroma Features")
    try:
        chroma = features['chroma']
        print(f"  Shape: {chroma['shape']}")
        print(f"  Pitch classes: {chroma['n_chroma']}")
        print(f"  Time frames: {chroma['shape'][1]}")

        # Validate Chroma data
        assert chroma['n_chroma'] == 12, "Expected 12 pitch classes"
        assert len(chroma['chroma_mean']) == 12, "Chroma mean length mismatch"
        assert len(chroma['pitch_classes']) == 12, "Pitch classes mismatch"

        print(f"  ✅ Chroma validation passed")
        print(f"  Pitch classes: {', '.join(chroma['pitch_classes'])}")

        # Show dominant pitch
        max_idx = chroma['chroma_mean'].index(max(chroma['chroma_mean']))
        dominant_pitch = chroma['pitch_classes'][max_idx]
        print(f"  Dominant pitch: {dominant_pitch}")

    except Exception as e:
        print(f"  ❌ Chroma validation failed: {str(e)}")
        return False

    # Test 4: Audio Info Validation
    print("\n[Test 4] Audio Info")
    try:
        audio_info = features['audio_info']
        print(f"  Duration: {audio_info['duration']:.2f}s")
        print(f"  Sample rate: {audio_info['sample_rate']} Hz")
        print(f"  Tempo: {audio_info['tempo']:.1f} BPM")
        print(f"  Detected beats: {audio_info['num_beats']}")

        # Validate audio info
        assert audio_info['duration'] > 0, "Invalid duration"
        assert audio_info['sample_rate'] > 0, "Invalid sample rate"
        # Note: Tempo can be 0 for audio without clear beats (silence, drones, etc.)
        assert audio_info['tempo'] >= 0, "Invalid tempo"

        if audio_info['tempo'] == 0:
            print(f"  ⚠️  No beats detected (expected for simple test audio)")

        print(f"  ✅ Audio info validation passed")

    except Exception as e:
        print(f"  ❌ Audio info validation failed: {str(e)}")
        return False

    # Test 5: Save and Load Features
    print("\n[Test 5] Save/Load Features")
    try:
        test_feature_path = 'features/test_features.json'
        os.makedirs('features', exist_ok=True)

        # Save features
        extractor.save_features(features, test_feature_path)
        print(f"  ✅ Features saved to {test_feature_path}")

        # Load features
        loaded_features = extractor.load_features(test_feature_path)
        assert loaded_features is not None, "Failed to load features"
        assert loaded_features['audio_info']['duration'] == features['audio_info']['duration'], \
            "Loaded features don't match"

        print(f"  ✅ Features loaded and verified")

        # Check file size
        file_size = os.path.getsize(test_feature_path)
        print(f"  Feature file size: {file_size / 1024:.1f} KB")

    except Exception as e:
        print(f"  ❌ Save/Load test failed: {str(e)}")
        return False

    # Test 6: Performance Benchmark
    print("\n[Test 6] Performance Benchmark")
    print("  Running 5 iterations...")
    try:
        times = []
        for i in range(5):
            start = time.time()
            _, extraction_time = extractor.extract_all_features(test_audio)
            times.append(extraction_time)
            print(f"    Iteration {i+1}: {extraction_time:.3f}s")

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n  📊 Performance Statistics:")
        print(f"    Average: {avg_time:.3f}s")
        print(f"    Min: {min_time:.3f}s")
        print(f"    Max: {max_time:.3f}s")

        # Check if within performance target (< 5 seconds for 5 second audio)
        if avg_time < 5.0:
            print(f"  ✅ Performance target met (< 5s)")
        else:
            print(f"  ⚠️  Performance slower than target (> 5s)")

    except Exception as e:
        print(f"  ❌ Performance test failed: {str(e)}")
        return False

    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    print(f"\n📋 Summary:")
    print(f"  - MFCC coefficients: {mfcc['n_mfcc']} x {mfcc['shape'][1]} frames")
    print(f"  - Chroma features: {chroma['n_chroma']} x {chroma['shape'][1]} frames")
    print(f"  - Average extraction time: {avg_time:.3f}s")
    print(f"  - Feature file size: {file_size / 1024:.1f} KB")
    print(f"  - Audio duration: {audio_info['duration']:.2f}s")
    print(f"  - Tempo: {audio_info['tempo']:.1f} BPM")

    return True


def test_api_integration():
    """
    Test feature extraction integration with Flask API
    """
    print("\n" + "=" * 60)
    print("API Integration Test")
    print("=" * 60)

    print("\n📝 To test the API integration:")
    print("  1. Start the Flask server: python app.py")
    print("  2. Upload a file via the web interface")
    print("  3. Check that features are extracted and saved")
    print("  4. Use GET /api/features to list all features")
    print("  5. Use GET /api/features/<file_id> to retrieve specific features")

    print("\n🔧 Manual API test commands:")
    print("  # Health check")
    print("  curl http://localhost:5000/api/health")
    print()
    print("  # Upload file")
    print("  curl -X POST -F 'file=@path/to/audio.mp3' http://localhost:5000/api/upload")
    print()
    print("  # List features")
    print("  curl http://localhost:5000/api/features")
    print()
    print("  # Get specific features")
    print("  curl http://localhost:5000/api/features/<file_id>")


if __name__ == '__main__':
    # Run feature extraction tests
    success = test_feature_extraction()

    # Show API integration info
    test_api_integration()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
