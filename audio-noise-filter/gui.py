from nicegui import app, ui
import audio_tools as tools 
import plotly.graph_objects as go
import asyncio


fig = go.Figure()
'''
label = ui.label('00').classes('text-h3')


async def start_timer():
    for i in range(11):  # 0 to 5 in steps of 0.5
        seconds = i * 0.5
        label.text = f'{seconds:04.1f}'
        await asyncio.sleep(0.5)

async def record_with_timer():
    ui.notify('Recording...')
    await asyncio.gather(start_timer(), tools.record_audio())
    ui.notify('Recording finished')
'''


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

        ui.label('Fillters').classes('text-h6')
        
        with ui.row().classes('items-center justify-center'):
            dropdown_btn = ui.dropdown_button(text='Filters', split=True)   
            with ui.row().classes('items-center justify-center'):
                with dropdown_btn:
                    ui.item('Fillter', on_click=lambda: (
                        tools.audio_noise_filter(fig),
                        ui.notify('Filtering done'),
                        dropdown_btn.set_text('Filter'),
                        plot.update()
                        ))
                ui.button('Play Filtered', on_click=lambda: (tools.play_fillter(), ui.notify('Playback done')
                    ))
                        
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
