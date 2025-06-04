"""
signal_processing.py
This module contains digital filtering operations (e.g., FFT, bandpass, etc.)
"""

import signal_tools as tools
import os
from scipy.io.wavfile import write, read 
import scipy.signal as signal
import numpy as np
import plotly.graph_objects as go
import config


INPUT_FILENAME, OUTPUT_FILENAME = config.INPUT_FILENAME, config.OUTPUT_FILENAME
fig_time, fig_freq = config.fig_time, config.fig_freq
# === Constants ===

        
def scaling(scale):
    
    """
    Apply a noise filter to the audio signal.
    input:
        scale: scaling factor to apply to the audio signal
    output:
        None, but writes the scaled signal to OUTPUT_FILENAME
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

def time_shift(shift_ms):
    
    #TODO: fix time shifting and add true phase shifting using fft
    """
    Apply a time shifting shift to the audio signal.
    input:
        shift_ms: time shift in milliseconds
    output:
        None, but writes the shifted signal to OUTPUT_FILENAME
    """
    try:
        rate, data = tools.open_signal(INPUT_FILENAME)
        time_shifted_data = np.roll(data, int(shift_ms * rate / 1000))
        write(OUTPUT_FILENAME, rate, time_shifted_data)
        print("Phase time shifting was applied.")
        
    except Exception as e:
        print(f"[ERROR] Failed to apply noise filter: {e}")

def fft(input_filename):
    
    """
    Apply Fast Fourier Transform (FFT) to input file audio signal.
    input:
        None
    output:
        freq: numpy array of frequencies
        magnitude: numpy array of magnitudes corresponding to the frequencies
    """
    
    try:
        print("Applying FFT...")
        rate, data = tools.open_signal(input_filename)
        fft_data = np.fft.fft(data)
        freq = np.fft.fftfreq(len(data), d=1 / rate)
        
        pos_mask = freq >= 0  # Only keep positive frequencies
        freq = freq[pos_mask]
        magnitude = np.abs(fft_data[pos_mask])
        magnitude_db = 20 * np.log10(magnitude)  # Convert to dB scale
        #magnitude_db = np.clip(magnitude_db, -100, 0)  # Clip to avoid log(0)
        
        print("FFT computed.")
        return freq, magnitude_db
    
    except Exception as e:
        print(f"[ERROR] Failed to compute FFT: {e}")
        return None, None

def apply_filter(data, rate, cutoff, btype, order=2):

    """
    Apply a Butterworth filter to the input signal.
    input:
        data: numpy array of audio signal data
        rate: sample rate of the audio signal
        cutoff: cutoff frequency or frequencies for the filter
        btype: type of filter ('lowpass', 'highpass', 'bandpass', 'bandstop')
        order: order of the filter
    output:
        filtered_data: numpy array of filtered audio signal data
    """
    try:
        nyquist = 0.5 * rate
        normal_cutoff = np.array(cutoff) / nyquist

        print(f"Normalized cutoff: {normal_cutoff}")
        print(f"Applying {btype} filter with cutoff: {cutoff}, order: {order}, rate: {rate}")
        print(f"[DEBUG] btype={btype}, cutoff={cutoff}, normal_cutoff={normal_cutoff}")

        #b, a = signal.butter(order, normal_cutoff, btype=btype, analog=False)
        
        if np.any(normal_cutoff <= 0) or np.any(normal_cutoff >= 1):
            raise ValueError(f"Invalid normalized cutoff: {normal_cutoff}")

        # Use second-order sections for numerical stability
        sos = signal.butter(order, normal_cutoff, btype=btype, analog=False, output='sos')
        filtered_data = signal.sosfiltfilt(sos, data)

        if np.isnan(filtered_data).any():
            raise ValueError("Filtered data contains NaNs")
        
        # Debugging information
        #print(f"[DEBUG] Filter coefficients - b: {b}, a: {a}")
        print(f"[DEBUG] sos coefficients: {sos}")
        print(f"[DEBUG] Data before filtering: {data[:10]}... (first 10 samples)")        
        print(f"[DEBUG] Data type after conversion: {data.dtype}")
        #filtered_data = signal.filtfilt(b, a, data)
        print(f'[DEBUG] Filtered data: {filtered_data[:10]}... (first 10 samples)')
        
        '''
        # Normalize to int16 range
        max_val = np.max(np.abs(filtered_data))
        if max_val > 0:
            filtered_data = (filtered_data / max_val) * 32767
        '''
        
        print(f"[DEBUG] Filtered data max value: {np.max(filtered_data)}, min value: {np.min(filtered_data)}")

        write(OUTPUT_FILENAME, rate, filtered_data.astype(np.int16))

        return filtered_data
    
    except Exception as e:
        print(f"[ERROR] Failed to apply filter: {e}")
        return None
    
def FIR(input_filename, cutoff, btype, order=2):
    
    """
    Apply a FIR filter to the input file audio signal.
    input:
        input_filename: path to the input audio file
        cutoff: cutoff frequency or frequencies for the filter
        btype: type of filter ('lowpass', 'highpass', 'bandpass', 'bandstop')
    output:
        filtered_data: numpy array of filtered audio signal data
    """
    try:
        rate, data = tools.open_signal(input_filename)
        nyquist = 0.5 * rate
        normal_cutoff = np.array(cutoff) / nyquist

        # Design the FIR filter
        taps = signal.firwin(numtaps=101, cutoff=normal_cutoff, window='hamming', pass_zero=btype)
        filtered_data = signal.filtfilt(taps, 1.0, data)

        write(OUTPUT_FILENAME, rate, filtered_data.astype(np.int16))
        return filtered_data

    except Exception as e:
        print(f"[ERROR] Failed to apply FIR filter: {e}")
        return None