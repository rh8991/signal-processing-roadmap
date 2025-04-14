import PySimpleGUI as sg

def create_window():
    layout = [
        [sg.Text('Signal Type:'), sg.Combo(['Sine', 'Square', 'Triangle'], default_value='Sine', key='type')],
        [sg.Text('Frequency (Hz):'), sg.InputText('440', key='freq')],
        [sg.Text('Amplitude (0-1):'), sg.InputText('0.5', key='amp')],
        [sg.Text('Duration (s):'), sg.InputText('2', key='duration')],
        [sg.Button('Generate & Plot'), sg.Button('Play'), sg.Button('Exit')],
    ]
    return sg.Window('Signal Generator', layout)
