import PySimpleGUI as sg

def create_window():
    layout = [
        [sg.Text('Signal Type:'), sg.Combo(['Sine', 'Square', 'Triangle', 'Sawtooth', 'Custom', 'Noise'], default_value='Sine', key='type')],
        [sg.Text('Frequency (Hz):'), sg.InputText('440', key='freq')],
        [sg.Text('Amplitude (0-1):'), sg.InputText('0.5', key='amp')],
        [sg.Text('Phase (rad):'), sg.InputText('0', key='phase')],
        [sg.Text('Offset:'), sg.InputText('0', key='offset')],
        [sg.Text('Duration (s):'), sg.InputText('2', key='duration')],
        [sg.Button('Generate & Plot'), sg.Button('Play'),sg.Button('Export'), sg.Button('Exit')],
    ]
    return sg.Window('Signal Generator', layout)
