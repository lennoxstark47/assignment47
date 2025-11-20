import { useState, useRef } from 'react'
import './App.css'

interface AudioFeatures {
  duration: number
  sampleRate: number
  channels: number
  rms: number
  zeroCrossingRate: number
  spectralCentroid: number
}

function App() {
  const [audioFile, setAudioFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [features, setFeatures] = useState<AudioFeatures | null>(null)
  const [waveformData, setWaveformData] = useState<number[]>([])
  const [error, setError] = useState<string | null>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const audioContextRef = useRef<AudioContext | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setAudioFile(file)
      setError(null)
      setFeatures(null)
    }
  }

  const calculateZeroCrossingRate = (audioData: Float32Array): number => {
    let crossings = 0
    for (let i = 1; i < audioData.length; i++) {
      if ((audioData[i] >= 0 && audioData[i - 1] < 0) || (audioData[i] < 0 && audioData[i - 1] >= 0)) {
        crossings++
      }
    }
    return crossings / audioData.length
  }

  const calculateRMS = (audioData: Float32Array): number => {
    let sum = 0
    for (let i = 0; i < audioData.length; i++) {
      sum += audioData[i] * audioData[i]
    }
    return Math.sqrt(sum / audioData.length)
  }

  const calculateSpectralCentroid = (audioBuffer: AudioBuffer): number => {
    const audioData = audioBuffer.getChannelData(0)
    const fftSize = 2048
    const audioCtx = audioContextRef.current!

    // Create an offline context for analysis
    const offlineCtx = new OfflineAudioContext(
      audioBuffer.numberOfChannels,
      audioBuffer.length,
      audioBuffer.sampleRate
    )

    const source = offlineCtx.createBufferSource()
    source.buffer = audioBuffer

    const analyser = offlineCtx.createAnalyser()
    analyser.fftSize = fftSize

    source.connect(analyser)
    analyser.connect(offlineCtx.destination)

    const frequencyData = new Uint8Array(analyser.frequencyBinCount)
    analyser.getByteFrequencyData(frequencyData)

    // Calculate spectral centroid
    let numerator = 0
    let denominator = 0

    for (let i = 0; i < frequencyData.length; i++) {
      const frequency = (i * audioBuffer.sampleRate) / fftSize
      const magnitude = frequencyData[i]
      numerator += frequency * magnitude
      denominator += magnitude
    }

    return denominator > 0 ? numerator / denominator : 0
  }

  const drawWaveform = (audioData: Float32Array) => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const width = canvas.width
    const height = canvas.height

    ctx.fillStyle = '#1a1a2e'
    ctx.fillRect(0, 0, width, height)

    ctx.strokeStyle = '#00d4ff'
    ctx.lineWidth = 2

    const step = Math.ceil(audioData.length / width)
    const amp = height / 2

    ctx.beginPath()
    for (let i = 0; i < width; i++) {
      const min = audioData.slice(i * step, (i + 1) * step).reduce((a, b) => Math.min(a, b), 1)
      const max = audioData.slice(i * step, (i + 1) * step).reduce((a, b) => Math.max(a, b), -1)

      ctx.lineTo(i, (1 + min) * amp)
      ctx.lineTo(i, (1 + max) * amp)
    }
    ctx.stroke()

    // Draw center line
    ctx.strokeStyle = '#ffffff33'
    ctx.lineWidth = 1
    ctx.beginPath()
    ctx.moveTo(0, height / 2)
    ctx.lineTo(width, height / 2)
    ctx.stroke()
  }

  const processAudio = async () => {
    if (!audioFile) {
      setError('Please select an audio file')
      return
    }

    setIsProcessing(true)
    setError(null)

    try {
      // Create AudioContext
      if (!audioContextRef.current) {
        audioContextRef.current = new AudioContext()
      }

      const audioContext = audioContextRef.current

      // Read file as ArrayBuffer
      const arrayBuffer = await audioFile.arrayBuffer()

      // Decode audio data
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer)

      // Get audio data from first channel
      const audioData = audioBuffer.getChannelData(0)

      // Calculate features
      const rms = calculateRMS(audioData)
      const zcr = calculateZeroCrossingRate(audioData)
      const spectralCentroid = calculateSpectralCentroid(audioBuffer)

      const extractedFeatures: AudioFeatures = {
        duration: audioBuffer.duration,
        sampleRate: audioBuffer.sampleRate,
        channels: audioBuffer.numberOfChannels,
        rms: rms,
        zeroCrossingRate: zcr,
        spectralCentroid: spectralCentroid
      }

      setFeatures(extractedFeatures)

      // Downsample for waveform display
      const displayData = new Float32Array(1000)
      const blockSize = Math.floor(audioData.length / 1000)
      for (let i = 0; i < 1000; i++) {
        const start = blockSize * i
        let sum = 0
        for (let j = 0; j < blockSize; j++) {
          sum += Math.abs(audioData[start + j])
        }
        displayData[i] = sum / blockSize
      }

      setWaveformData(Array.from(displayData))
      drawWaveform(audioData)

      console.log('Audio processing completed:', extractedFeatures)
    } catch (err) {
      console.error('Error processing audio:', err)
      setError(err instanceof Error ? err.message : 'Failed to process audio')
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎵 Web Audio API Experiment</h1>
        <p>Client-side audio feature extraction using Web Audio API</p>
      </header>

      <div className="container">
        <div className="upload-section">
          <h2>Upload Audio File</h2>
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            className="file-input"
          />
          {audioFile && (
            <div className="file-info">
              <p>📁 Selected: <strong>{audioFile.name}</strong></p>
              <p>Size: {(audioFile.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          )}
          <button
            onClick={processAudio}
            disabled={!audioFile || isProcessing}
            className="process-button"
          >
            {isProcessing ? 'Processing...' : 'Extract Features'}
          </button>
        </div>

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {features && (
          <div className="results">
            <h2>📊 Extracted Features</h2>

            <div className="features-grid">
              <div className="feature-card">
                <h3>Duration</h3>
                <p className="feature-value">{features.duration.toFixed(2)}s</p>
              </div>

              <div className="feature-card">
                <h3>Sample Rate</h3>
                <p className="feature-value">{features.sampleRate} Hz</p>
              </div>

              <div className="feature-card">
                <h3>Channels</h3>
                <p className="feature-value">{features.channels}</p>
              </div>

              <div className="feature-card">
                <h3>RMS Energy</h3>
                <p className="feature-value">{features.rms.toFixed(6)}</p>
                <p className="feature-desc">Root Mean Square amplitude</p>
              </div>

              <div className="feature-card">
                <h3>Zero Crossing Rate</h3>
                <p className="feature-value">{features.zeroCrossingRate.toFixed(6)}</p>
                <p className="feature-desc">Rate of sign changes</p>
              </div>

              <div className="feature-card">
                <h3>Spectral Centroid</h3>
                <p className="feature-value">{features.spectralCentroid.toFixed(2)} Hz</p>
                <p className="feature-desc">Brightness measure</p>
              </div>
            </div>

            <div className="waveform-section">
              <h3>Waveform Visualization</h3>
              <canvas
                ref={canvasRef}
                width={800}
                height={200}
                className="waveform-canvas"
              />
            </div>
          </div>
        )}

        <div className="info-section">
          <h2>ℹ️ About This Experiment</h2>
          <p>
            This experiment demonstrates client-side audio processing using the Web Audio API.
            It extracts basic audio features that can be used for similarity detection:
          </p>
          <ul>
            <li><strong>RMS Energy:</strong> Overall loudness/energy of the audio</li>
            <li><strong>Zero Crossing Rate:</strong> Indicates noisiness vs. tonality</li>
            <li><strong>Spectral Centroid:</strong> Indicates brightness of the sound</li>
          </ul>
          <p className="note">
            <strong>Note:</strong> Web Audio API provides basic features but lacks advanced
            capabilities like MFCC and chromagram extraction that are available in Librosa.
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
