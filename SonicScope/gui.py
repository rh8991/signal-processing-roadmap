from nicegui import app, ui
import signal_tools as tools 
import plotly.graph_objects as go
import signal_processing as sp
import config

INPUT_FILENAME ,OUTPUT_FILENAME = config.INPUT_FILENAME ,config.OUTPUT_FILENAME

fig_time = config.fig_time
fig_freq = config.fig_freq

# === Functions ===
def clear_plots():
    print("Cleaning plots")
    fig_time.data = []
    fig_freq.data = []

    plot_time.update()
    plot_freq.update()

    ui.notify('Plots cleared')
    print("Plots cleared")


# === GUI ===


    
with ui.row().classes('items-start'):
    with ui.column().classes('items-left justify-center q-pa-md gap-4'):
        with ui.row().classes('items-center justify-center'):
            ui.image(config.logo).classes('w-20 h-20')
            ui.label('SonicScope').classes('text-h6')
        
        with ui.row().classes('items-center justify-center'):   
            ui.label('Input').classes('text-h6')
            
        with ui.row().classes('items-center justify-center'):
            ui.button('🔴 Record', on_click=lambda: (
                ui.notify('Recording...'),
                tools.record_audio(), 
                ui.notify('Recording finished')))
            ui.button('▶️ Play', on_click=lambda: (tools.play_signal(INPUT_FILENAME), ui.notify('Playback done')))
            ui.button('📈 Plot', on_click=lambda: (
                fig_time.data == [],
                ui.notify('Plotting'),
                tools.plot_Input_signal(),
                plot_time.update()
                ))
            
            ui.button('🗑️ Clear', on_click= clear_plots)    
                
        with ui.row().classes('items-center justify-center' ):
            ui.upload(on_upload=tools.upload_signal, label='🎵 Load WAV File')

        with ui.row().classes('items-left justify-center'):
            ui.label('Output').classes('text-h6')
            
        with ui.row().classes('items-center justify-center'):
            scale_in = ui.number(label='Scale', value=1, min=0, max=2, step=0.1)
            t_shift_in = ui.number(label='Time shifting [ms]',value=0, min=0, step=1)
            
            ui.button('Generate', on_click=lambda: (
                sp.time_shift(t_shift_in.value), print(f"TIME SHIFTING {t_shift_in.value}") if t_shift_in.value > 0 else None, #! TODO: fix time shifting
                sp.scaling(scale_in.value), print(f"SCALING {scale_in.value}") if scale_in.value != 1 else None,
                tools.add_output(),
                plot_time.update()))
            
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
                
                ui.button('FFT',icon='timeline', on_click=lambda: (
                            print("applying FFT..."),
                            dropdown_btn.set_text('FFT'),
                            dropdown_btn.close(),
                            sp.fft(),
                            plot_freq.update(),
                            ))
                
                ui.button('▶️ Play', on_click=lambda: (tools.play_signal(OUTPUT_FILENAME), ui.notify('Playback done')))
                    
    with ui.column().classes('q-pa-md'):
        with ui.tabs() as tabs:
            ui.tab('Time Domain', icon='timeline')
            ui.tab('Frequency Domain', icon='timeline')
            
        with ui.tab_panels(tabs, value='Time Domain'):#.classes('w-full'):
            with ui.tab_panel('Time Domain'):
                fig_time.update_layout(
                    legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='right', x=1),
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title='Time (s)',
                    yaxis_title='Amplitude')
                    
                plot_time = ui.plotly(fig_time).classes('w-full h-80')
                            
            with ui.tab_panel('Frequency Domain'):
                fig_freq.update_layout(
                    legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='right', x=1),
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title='Frequency (Hz)',
                    yaxis_title='FFT Amplitude')
                
                plot_freq = ui.plotly(fig_freq).classes('w-full h-80')
        
          
with ui.footer().classes('items-center justify-center q-pa-none q-mt-none').style('height: 30px;'):
    ui.label('SonicScope – Developed by Ronel Herzass').classes('text-caption q-mb-none').style('line-height: 1; margin: 0; padding: 0')


ui.run()
