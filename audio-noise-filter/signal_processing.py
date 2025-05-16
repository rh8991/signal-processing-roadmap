"""
signal_processing.py
This module contains digital filtering operations (e.g., FFT, bandpass, etc.)
"""

import signal_tools as tools
import os
from scipy.io.wavfile import write, read
import numpy as np



INPUT_FILENAME = tools.INPUT_FILENAME
OUTPUT_FILENAME = tools.OUTPUT_FILENAME

        
def scaling(fig, scale):
    """
    Apply a noise filter to the audio signal.
    """
    try:
        rate, data = tools.open_signal(INPUT_FILENAME)
        scaled_data = (data * float(scale)).astype(np.int16)  # Scale the data
        if np.max(scaled_data) > 32767 or np.min(scaled_data) < -32768:
            scaled_data = np.clip(scaled_data, -32768, 32767)
            print("Clipping applied to scaled data.")
        
        scaled_data = np.ascontiguousarray(scaled_data)
        write(OUTPUT_FILENAME, rate, scaled_data)
        print("Scaling was applied.")
        
    except Exception as e:
        print(f"[ERROR] Failed to apply noise scaling: {e}")

def time_shift(fig, shift_ms):
    #TODO: fix time shifting and add true phase shifting using fft
    """
    Apply a time shifting shift to the audio signal.
    """
    try:
        rate, data = tools.open_signal(INPUT_FILENAME)
        time_shifted_data = np.roll(data, int(shift_ms * rate / 1000))
        write(OUTPUT_FILENAME, rate, time_shifted_data)
        print("Phase time shifting was applied.")
        
    except Exception as e:
        print(f"[ERROR] Failed to apply noise filter: {e}")

def fft(fig):
    """
    Apply Fast Fourier Transform (FFT) to the audio signal.
    """
#try:
    rate, data = tools.open_signal()
    fft_data = np.fft.fft(data)
    #write(OUTPUT_FILENAME, rate, fft_data)
    #tools.add_trace(fig)
    print("FFT was applied.")
    
    #except Exception as e:
    #    print(f"[ERROR] Failed to apply FFT: {e}")
