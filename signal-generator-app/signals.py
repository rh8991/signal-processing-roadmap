import numpy as np

def generate_sine(freq, amp, phase, offset, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    return t, amp * np.sin(2 * np.pi * freq * t + phase) + offset

def generate_square(freq, amp, phase, offset, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    return t, amp * np.sign(np.sin(2 * np.pi * freq * t + phase)) + offset

def generate_triangle(freq, amp, phase, offset, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    t_shifted = t + phase / (2 * np.pi * freq)
    return t, amp * (2 * np.abs(2 * (t_shifted * freq - np.floor(t_shifted * freq + 0.5))) - 1) + offset

def generate_sawtooth(freq, amp, phase, offset, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    t_shifted = t + phase / (2 * np.pi * freq)
    return t, amp * (2 * (t_shifted * freq - np.floor(t_shifted * freq + 0.5))) + offset