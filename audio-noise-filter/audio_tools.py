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


def play_audio():
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

def play_fillter():
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

def audio_upload(e):
    #print(e.content.read())
    with open(INPUT_FILENAME, 'wb') as f:
        f.write(e.content.read())

    rate, data = read(INPUT_FILENAME)
    nicegui.notify(f"Loaded {e.name}: {data.shape[0]/rate:.2f} sec")


def plot_audio_signal(fig):
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

def audio_noise_filter(fig):
    """
    Apply a noise filter to the audio signal.
    """
    try:
        print("Applying noise filter...")
        if not os.path.exists(INPUT_FILENAME):
            print(f"[ERROR] File '{INPUT_FILENAME}' does not exist.")
            return
        rate, data = read(INPUT_FILENAME)
        # Apply a simple noise filter (e.g., low-pass filter)
        # This is just a placeholder; actual implementation would depend on the desired filter
        data = np.fromstring(data, dtype=np.int16)
        if len(data.shape) > 1:
            data = data[:, 0]
        filtered_data = data * 0.5  # Example: reduce amplitude by half
        write(OUTPUT_FILENAME, rate, filtered_data)
        add_trace(fig)
        print("Noise filter applied.")
        
    except Exception as e:
        print(f"[ERROR] Failed to apply noise filter: {e}")
        
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
        fig.add_trace(go.Scatter(x=t, y=data / 32767, mode='lines', name='Filtered Signal'))
        print("Trace added.")
        
    except Exception as e:
        print(f"[ERROR] Failed to add trace: {e}")
        