from nicegui import app, ui
import signal_tools as tools 
import plotly.graph_objects as go
import signal_processing as sp

INPUT_FILENAME = tools.INPUT_FILENAME
OUTPUT_FILENAME = tools.OUTPUT_FILENAME

fig = go.Figure()

with ui.row().classes('items-start'):
    with ui.column().classes('items-left justify-center q-pa-md gap-4'):
        with ui.row().classes('items-center justify-center'):
            ui.image('audio-noise-filter/assets/ANF_logo.png').classes('w-32 h-32')
            ui.label('Audio Player').classes('text-h4')
        
        with ui.row().classes('items-center justify-center'):   
            ui.label('Input').classes('text-h6')
            
        with ui.row().classes('items-center justify-center'):
            ui.button('🔴 Record', on_click=lambda: (
                ui.notify('Recording...'),
                tools.record_audio(), 
                ui.notify('Recording finished')))
            ui.button('▶️ Play', on_click=lambda: (tools.play_signal(INPUT_FILENAME), ui.notify('Playback done')))
            ui.button('📈 Plot', on_click=lambda: (
                fig.data == [],
                ui.notify('Plotting'),
                tools.plot_Input_signal(fig),
                plot.update()
                ))
            
        with ui.row().classes('items-center justify-center' ):
            ui.upload(on_upload=tools.upload_signal, label='🎵 Load WAV File')

        ui.label('Output').classes('text-h6')
        
        with ui.row().classes('items-center justify-center'):
            scale_in = ui.number(label='Scale', value=1, min=0, max=2, step=0.1)
            t_shift_in = ui.number(label='Time shifting [ms]',value=0, min=0, step=1)
            
            ui.button('Generate', on_click=lambda: (
                sp.time_shift(fig, t_shift_in.value), print(f"TIME SHIFTING {t_shift_in.value}") if t_shift_in.value > 0 else None, #! TODO: fix time shifting
                sp.scaling(fig, scale_in.value), print(f"SCALING {scale_in.value}") if scale_in.value != 1 else None,
                tools.add_trace(fig),
                plot.update()))
            
        with ui.row().classes('items-center justify-center'):
            dropdown_btn = ui.dropdown_button(text='Filters', split=True)   
            with ui.row().classes('items-center justify-center'):
                with dropdown_btn:
                    ui.item('High-Pass', on_click=lambda: (
                        dropdown_btn.set_text('High-Pass'),
                        dropdown_btn.close()
                        ))
                    ui.item('Low-Pass', on_click=lambda: (
                        dropdown_btn.set_text('Low-Pass'),
                        dropdown_btn.close()
                        ))
                    ui.item('Band-Pass', on_click=lambda: (
                        dropdown_btn.set_text('Band-Pass'),
                        dropdown_btn.close()
                        ))
                    ui.item('Band-Stop', on_click=lambda: (
                        dropdown_btn.set_text('Band-Stop'),
                        dropdown_btn.close()
                        ))
                    ui.item('FIR', on_click=lambda: (
                        dropdown_btn.set_text('FIR'),
                        dropdown_btn.close()
                    ))
                    ui.item('IIR', on_click=lambda: (
                        dropdown_btn.set_text('IIR'),
                        dropdown_btn.close()
                                                     ))
                    ui.item('FFT', on_click=lambda: (
                        dropdown_btn.set_text('FFT'),
                        dropdown_btn.close(),
                        sp.fft(fig),
                        plot.update(),
                        ))
                
                ui.button('▶️ Play', on_click=lambda: (tools.play_signal(OUTPUT_FILENAME), ui.notify('Playback done')))
                        
    with ui.column().classes('q-pa-md'):
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title='Time (s)',
            yaxis_title='Amplitude',
            title=dict(text='Audio Signal', x=0.5, y=0.95)
        )
        plot = ui.plotly(fig).classes('w-full h-full')                
        
          
with ui.footer().classes('items-center justify-center q-pa-md'):
    ui.label('Real-time Audio Noise Filter').classes('text-h6')
    ui.label('Developed by Ronel Herzass').classes('text-body2')

ui.run()
