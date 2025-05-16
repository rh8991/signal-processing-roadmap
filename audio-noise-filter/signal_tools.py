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


def play_signal():
    """
    Play the recorded audio from the WAV file.
    """
    try:
        if not os.path.exists(INPUT_FILENAME):
            print(f"[ERROR] File '{INPUT_FILENAME}' does not exist.")
            return

        print("Playing audio...")
        rate, data = read(INPUT_FILENAME)
        sd.play(data, rate)
        sd.wait()
        print("Playback finished.")
    except Exception as e:
        print(f"[ERROR] Failed to play audio: {e}")

def play_output():
    """
    Play the filtered audio from the WAV file.
    """
    try:
        if not os.path.exists(OUTPUT_FILENAME):
            print(f"[ERROR] File '{OUTPUT_FILENAME}' does not exist.")
            return

        print("Playing filtered audio...")
        rate, data = read(OUTPUT_FILENAME)
        sd.play(data, rate)
        sd.wait()
        print("Playback finished.")
    except Exception as e:
        print(f"[ERROR] Failed to play filtered audio: {e}")

def upload_signal(e):
    #print(e.content.read())
    with open(INPUT_FILENAME, 'wb') as f:
        f.write(e.content.read())

    rate, data = read(INPUT_FILENAME)
    nicegui.notify(f"Loaded {e.name}: {data.shape[0]/rate:.2f} sec")


def plot_signal(fig):
    """
    Plot the audio signal on the provided figure.
    """
    try:
        print("Plotting audio signal...")
        if not os.path.exists(INPUT_FILENAME):
            print(f"[ERROR] File '{INPUT_FILENAME}' does not exist.")
            return
        rate, data = read(INPUT_FILENAME)
        data = np.fromstring(data, dtype=np.int16)
        if len(data.shape) > 1:
            data = data[:, 0]  # Use only the first channel if stereo
            
        t = np.linspace(0, len(data) / rate, num=len(data))
        fig.data = []  # Clear previous data
        fig.add_trace(go.Scatter(x=t, y=data / 32767, mode='lines', name='Audio Signal'))
        print("Audio signal plotted.")
        
    except Exception as e:
        print(f"[ERROR] Failed to plot audio signal: {e}")

        
def add_trace(fig):
    """
    Add a trace to the figure.
    """
    try:
        print("Adding trace...")
        if not os.path.exists(OUTPUT_FILENAME):
            print(f"[ERROR] File '{OUTPUT_FILENAME}' does not exist.")
            return
        
        rate, data = read(OUTPUT_FILENAME)
        data = np.fromstring(data, dtype=np.int16)
        if len(data.shape) > 1:
            data = data[:, 0]  # Use only the first channel if stereo
            
        t = np.linspace(0, len(data) / rate, num=len(data))
        #data must be between -1 and 1 for plotting. int16 is between -32768 and 32767
        fig.add_trace(go.Scatter(x=t, y=data / 32767, mode='lines', name='Output Signal'))
        print("Trace added.")
        
    except Exception as e:
        print(f"[ERROR] Failed to add trace: {e}")
        
def open_signal():
    """
    Open the audio signal from the input file.
    """
    try:
        print("Applying noise filter...")
        if not os.path.exists(INPUT_FILENAME):
            print(f"[ERROR] File '{INPUT_FILENAME}' does not exist.")
            return
        rate, data = read(INPUT_FILENAME)
        if len(data.shape) > 1:
            data = data[:, 0]
        data = np.fromstring(data, dtype=np.int16)
        
        print(data.dtype, data.shape, np.max(data), np.min(data))
        
        return rate, data
    
    except Exception as e:
        print(f"[ERROR] Failed to read audio file: {e}")
        return None, None

def scaling(fig, scale):
    """
    Apply a noise filter to the audio signal.
    """
    try:
        rate, data = open_signal()
        scaled_data = (data * float(scale)).astype(np.int16)  # Scale the data
        if np.max(scaled_data) > 32767 or np.min(scaled_data) < -32768:
            scaled_data = np.clip(scaled_data, -32768, 32767)
            print("Clipping applied to scaled data.")
        write(OUTPUT_FILENAME, rate, scaled_data)
        add_trace(fig)
        print("Scaling was applied.")
        
    except Exception as e:
        print(f"[ERROR] Failed to apply noise filter: {e}")

def phase_shift(fig, phase):
    """
    Apply a phase shift to the audio signal.
    """
    try:
        rate, data = open_signal()
        phase_shifted_data = np.roll(data, int(phase))
        write(OUTPUT_FILENAME, rate, phase_shifted_data)
        add_trace(fig)
        print("Phase shift was applied.")
        
    except Exception as e:
        print(f"[ERROR] Failed to apply noise filter: {e}")
        