from nicegui import app, ui
import signal_tools as tools 
import plotly.graph_objects as go
import filters


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
            ui.button('▶️ Play', on_click=lambda: (tools.play_audio(), ui.notify('Playback done')))
            ui.button('📈 Plot', on_click=lambda: (
                fig.data == [],
                ui.notify('Plotting'),
                tools.plot_audio_signal(fig),
                plot.update()
                ))
            
        with ui.row().classes('items-center justify-center' ):
            ui.upload(on_upload=tools.audio_upload, label='🎵 Load WAV File')

        ui.label('Output').classes('text-h6')
        
        with ui.row().classes('items-center justify-center'):
            scale_in = ui.number(label='Scale', value=0.5, min=0, max=2, step=0.1,on_change= lambda e: scale_in.set_value(e.value))
            phase_in = ui.number(label='Phase',value=0, min=0, max=10, step=1,on_change= lambda e: phase_in.set_value(e.value))
            ui.button('Generate', on_click=lambda: (
                tools.phase_shift(fig, phase_in.value),
                tools.scaling(fig, scale_in.value),
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
                        filters.fft(fig),
                        plot.update(),
                        ))
                
                ui.button('▶️ Play', on_click=lambda: (tools.play_fillter(), ui.notify('Playback done')))
                        
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
