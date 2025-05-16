"""
signal_tools.py
Utility functions for recording, playing, loading, and manipulating signals.
"""

import sounddevice as sd
from scipy.io.wavfile import write, read
import numpy as np
import os
import nicegui
import plotly.graph_objects as go


# === Constants ===
SAMPLE_RATE = 44100  # in Hz
CHANNELS = 2
DURATION = 5  # seconds
INPUT_FILENAME = "audio-noise-filter/assets/input.wav"
OUTPUT_FILENAME = "audio-noise-filter/assets/output.wav"

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
        rate, data = read(filename)
        print("Sample rate:", rate)
        print(f"Original length: {len(data)}")  # should be 220500

        if len(data.shape) > 1:
            data = data[:, 0]  # Use only the first channel if stere
                    
        return rate, data
    
    except Exception as e:
        print(f"[ERROR] Failed to read input signal (input.wav): {e}")
        return None, None

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
    
    print(f"Uploading {e.name}...")
    with open(INPUT_FILENAME, 'wb') as f:
        f.write(e.content.read())

    rate, data = read(INPUT_FILENAME)
    nicegui.notify(f"Loaded {e.name}: {data.shape[0]/rate:.2f} sec")



# === Plotting ===
def plot_Input_signal(fig):
    """
    Plot the signal on the provided figure.
    """
    
    try:
        print("Plotting signal...")
        rate, data = open_signal(INPUT_FILENAME)
        if len(data.shape) > 1:
            data = data[:, 0]  # Use only the first channel if stereo
            
        t = np.linspace(0, len(data) / rate, num=len(data))
        fig.data = []  # Clear previous data
        fig.add_trace(go.Scatter(x=t, y=data / 32767, mode='lines', name='Input Signal'))
        print("Signal plotted.")
        
    except Exception as e:
        print(f"[ERROR] Failed to plot signal: {e}")
        
def add_trace(fig):
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
        fig.add_trace(go.Scatter(x=t, y=data / 32767, mode='lines', name='Output Signal'))
        print("Trace added.")
        
    except Exception as e:
        print(f"[ERROR] Failed to add trace: {e}")
        



        