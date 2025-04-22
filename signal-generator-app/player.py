# signal-generator-app/player.py
# This module is responsible for playing the generated audio signal.
# It uses the sounddevice library to play the audio signal through the default output device.

# The play_signal function takes the generated signal and the sampling frequency as input parameters.
import sounddevice as sd
from scipy.io.wavfile import write 
import PySimpleGUI as sg

def play_signal(signal, fs):
    sd.play(signal, fs)
    sd.wait()
    
# This function exports the generated signal to a WAV file.
# It uses the scipy.io.wavfile module to write the signal to a file.
def export_signal(signal, fs):
    filename = sg.popup_get_file('Save as', save_as=True, file_types=(('WAV Files', '*.wav'),), no_window=True)
    if filename:
        if not filename.endswith('.wav'):
            filename += '.wav'
        # Ensure the signal is in the correct format for writing
        signal = (signal * 32767).astype('int16')
        # Write the signal to a WAV file    
        write(filename, fs, signal)
        sg.popup('Signal exported successfully!')
    else:
        sg.popup('Export cancelled!')