from gui import create_window
import PySimpleGUI as sg
from signals import generate_sine, generate_square, generate_triangle, generate_sawtooth
from plotter import plot_signal
import player

fs = 44100  # Sampling frequency
window = create_window()
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED,'Exit'):
        break
    
    if event == 'Generate & Plot':
        signal_type = values['type']
        freq = float(values['freq'])
        amp = float(values['amp'])
        duration = float(values['duration'])
        phase = float(values['phase'])
        offset = float(values['offset'])

        if signal_type == 'Sine':
            t, signal = generate_sine(freq, amp, phase, offset, duration, fs)
        elif signal_type == 'Square':
            t, signal = generate_square(freq, amp, phase, offset, duration, fs)
        elif signal_type == 'Triangle':
            t, signal = generate_triangle(freq, amp, phase, offset, duration, fs)
        elif signal_type == 'Sawtooth':
            t, signal = generate_sawtooth(freq, amp, phase, offset, duration, fs)
        elif signal_type == 'Custom':
            # Custom signal generation logic can be added here
            sg.popup_error('Custom signal generation not implemented yet!')
            continue
        elif signal_type == 'Noise':
            # Noise signal generation logic can be added here
            sg.popup_error('Noise signal generation not implemented yet!')
            continue
        else:
            sg.popup_error('Unsupported signal type!')
            continue

        plot_signal(t, signal, title=f"{signal_type} Wave")
    elif event == 'Play':
        player.play_signal(signal, fs)
    elif event == 'Export':
        player.export_signal(signal, fs)
    elif event == 'Exit':
        break
window.close()