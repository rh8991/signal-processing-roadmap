# signal-generator-app/player.py
# This module is responsible for playing the generated audio signal.
import simpleaudio as sa
import numpy as np

def play_signal(signal, fs):
    # Ensure that highest value is in 16-bit range
    audio = signal * (2**15 - 1) / np.max(np.abs(signal))
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()