import numpy as np

def generate_sine(freq, amp, phase, duration, fs):
    t = np.linspace(0, duration, int(fs* duration), endpoint=False)
    return t, amp*np.sin(2 * np.pi * freq * t + phase)

def generate_square(freq, amp, phase, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    return t, amp * np.sign(np.sin(2 * np.pi * freq * t + phase))

def generate_triangle(freq, amp, phase, duration, fs):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    return t, amp * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1) + phase