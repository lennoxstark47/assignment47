"""
Simple test script for audio upload endpoint
Week 17/11/25
"""

import requests
import os

def test_upload():
    """Test the upload endpoint with the test audio file"""

    url = 'http://localhost:5000/api/upload'
    test_file = 'experiments/test_audio.wav'

    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False

    print("Testing audio upload endpoint...")
    print(f"File: {test_file}")
    print(f"Size: {os.path.getsize(test_file)} bytes")
    print()

    try:
        # Open and send file
        with open(test_file, 'rb') as f:
            files = {'file': ('test_audio.wav', f, 'audio/wav')}
            response = requests.post(url, files=files, timeout=30)

        # Check response
        if response.status_code == 200:
            data = response.json()
            print("✅ Upload successful!")
            print(f"   Filename: {data['filename']}")
            print(f"   Duration: {data['duration']:.2f} seconds")
            print(f"   Sample Rate: {data['sample_rate']} Hz")
            print(f"   Total Samples: {data['num_samples']:,}")
            print(f"   RMS Energy: {data['rms']:.4f}")
            print(f"   Waveform samples: {len(data['waveform'])} points")
            return True
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"   Error: {response.json().get('error', 'Unknown error')}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running on port 5000.")
        print("   Start the server with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_health():
    """Test the health check endpoint"""
    url = 'http://localhost:5000/api/health'

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['message']}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Audio Upload & Waveform Display - Test Script")
    print("Week 17/11/25")
    print("=" * 60)
    print()

    # Test health endpoint
    print("1. Testing health endpoint...")
    if test_health():
        print()

        # Test upload
        print("2. Testing upload endpoint...")
        test_upload()
    else:
        print()
        print("Server is not running. Start it with:")
        print("  python app.py")

    print()
    print("=" * 60)
