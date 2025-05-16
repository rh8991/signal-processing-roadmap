import signal_tools
import os
from scipy.io.wavfile import write, read
import numpy as np



INPUT_FILENAME = signal_tools.INPUT_FILENAME
OUTPUT_FILENAME = signal_tools.OUTPUT_FILENAME

        
def fft(fig):
    """
    Apply Fast Fourier Transform (FFT) to the audio signal.
    """
#try:
    rate, data = signal_tools.open_signal()
    fft_data = np.fft.fft(data)
        #write(OUTPUT_FILENAME, rate, fft_data)
    signal_tools.add_trace(fig)
    print("FFT was applied.")
    
    #except Exception as e:
    #    print(f"[ERROR] Failed to apply FFT: {e}")
