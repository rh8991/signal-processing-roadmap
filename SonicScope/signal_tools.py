"""
signal_tools.py
Utility functions for recording, playing, loading, and manipulating signals.
"""

import sounddevice as sd
from scipy.io.wavfile import write, read
import numpy as np
import os
import plotly.graph_objects as go
from pydub import AudioSegment
import config
import signal_processing as sp
# === Imports ===

# === Constants ===
SAMPLE_RATE = 44100  # in Hz
CHANNELS = 2
DURATION = 5  # seconds
INPUT_FILENAME = config.INPUT_FILENAME
OUTPUT_FILENAME = config.OUTPUT_FILENAME
fig_time = config.fig_time
fig_freq = config.fig_freq

# === Open Signal === 
def open_signal(filename):
    
    """
    Open the signal from the input file.
    """
    
    try:
        
        print(f"Opening signal from {filename}")
        if not os.path.exists(filename):
            print(f"[ERROR] File '{filename}' does not exist.")
            return
        rate, data = read(convert_to_pcm16(filename))
        print("Sample rate:", rate)
        print(f"Original length: {len(data)}")  # should be 220500

        if len(data.shape) > 1:
            data = data[:, 0]  # Use only the first channel if stere
                    
        return rate, data
    
    except Exception as e:
        print(f"[ERROR] Failed to read input signal (input.wav): {e}")
        return None, None

def save_signal(data, rate):
   
    """
    Save the signal data to the output file.
    """
    
    try:
        print(f"Saving signal to {OUTPUT_FILENAME}")
        os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)
        write(OUTPUT_FILENAME, rate, data.astype(np.int16))
        print("Signal saved successfully.")
        
    except Exception as e:
        print(f"[ERROR] Failed to save output signal: {e}")
        
def convert_to_pcm16(input_path: str) -> str:
    
    """
    Convert any WAV file to PCM 16-bit format using pydub.
    Returns the path to the converted file (or original if already PCM).
    """
    
    sound = AudioSegment.from_file(input_path, format="wav")

    # Check if already 16-bit PCM
    if sound.sample_width == 2 and sound.frame_rate in [8000, 16000, 44100, 48000]:
        return input_path

    # Export as PCM 16-bit
    print(f"Converting {input_path} to PCM 16-bit format")
    sound = sound.set_sample_width(2)  # 2 bytes = 16 bits
    sound.export(input_path, format="wav")

    return input_path

# === Signal Input ===
def record_audio():
    
    """
    Record audio from the microphone and save it to a WAV file.
    """
    
    try:
        print("Recording...")
        recording = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16'
        )
        sd.wait()
        os.makedirs(os.path.dirname(INPUT_FILENAME), exist_ok=True)
        write(INPUT_FILENAME, SAMPLE_RATE, recording)
        print(f"Recording finished. Saved to {INPUT_FILENAME}")
    
    except Exception as e:
        print(f"[ERROR] Failed to record audio: {e}")


def play_signal(filename):
    
    """
    Play the recorded signal from the WAV file.
    input: filename - path to the WAV file
    output: plays the audio signal
    """
    
    try:
        rate, data = open_signal(filename)
        print(f"Playing signal from {filename}")
        print(f"Data shape: {data.shape}, dtype: {data.dtype}, Sample rate: {rate}")
        sd.play(data, rate)
        sd.wait()
        print("Playback finished.")
        
    except Exception as e:
        print(f"[ERROR] Failed to play audio: {e}")
        
        
def upload_signal(e):
    
    """
    Upload a signal file from the user.
    """
    
    print(f"Uploading {e.name}...")
    with open(INPUT_FILENAME, 'wb') as f:
        f.write(e.content.read())

    rate, data = read(convert_to_pcm16(INPUT_FILENAME))



# === Plotting ===
def plot_Input_signal():
    
    """
    Plot the signal on the provided figure.
    """
    
    try:
        print("Plotting signal...")
        rate, data = open_signal(INPUT_FILENAME)
        if len(data.shape) > 1:
            data = data[:, 0]  # Use only the first channel if stereo
            
        t = np.linspace(0, len(data) / rate, num=len(data))
        fig_time.add_trace(go.Scatter(x=t, y=data / 32767, mode='lines', name='Input Signal'))
        fig_time.update()
        print("Signal plotted.")
        
    except Exception as e:
        print(f"[ERROR] Failed to plot signal: {e}")
        
def add_output():
    
    """
    Add a output.wav as a trace to the figure.
    """
    
    try:
        print("Adding trace...")
        
        rate, data = open_signal(OUTPUT_FILENAME)
        if len(data.shape) > 1:
            data = data[:, 0]  # Use only the first channel if stereo
            
        t = np.linspace(0, len(data) / rate, num=len(data))
        #data must be between -1 and 1 for plotting. int16 is between -32768 and 32767
        fig_time.add_trace(go.Scatter(x=t, y=data / 32767, mode='lines', name='Output Signal'))
        fig_time.update()
        print("Trace added.")
        
    except Exception as e:
        print(f"[ERROR] Failed to add trace: {e}")
        
def add_fft_trace(trace_name, filename):
    """
    Add a FFT trace to the frequency figure using a windowed signal and dB scaling.
    Only positive frequencies are shown.
    """
    try:
        print(f"Adding FFT trace from {filename}...")
        rate, data = open_signal(filename)
        if data is None:
            print("[ERROR] No data to add FFT trace.")
            return

        # Apply Hamming window - Because the FFT is sensitive to discontinuities, we apply a window function
        window = np.hamming(len(data))
        windowed_data = data * window

        fft_data = np.fft.fft(windowed_data)
        freq = np.fft.fftfreq(len(data), d=1 / rate)
        mask = freq >= 0
        freq = freq[mask] # Only keep positive frequencies
        magnitude = np.abs(fft_data)[mask]
        #magnitude_db = 20 * np.log10(magnitude/ np.max(magnitude))  # Convert to dB scale

        fig_freq.add_trace(go.Scatter(x=freq, y=magnitude, mode='lines', name=trace_name))
        fig_freq.update()
        print("FFT trace added.")

    except Exception as e:
        print(f"[ERROR] Failed to add FFT trace: {e}")



        