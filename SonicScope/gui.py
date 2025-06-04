from nicegui import app, ui, context, run
import signal_tools as tools 
import plotly.graph_objects as go
import signal_processing as sp
import config
import asyncio

INPUT_FILENAME, OUTPUT_FILENAME = config.INPUT_FILENAME, config.OUTPUT_FILENAME
fig_time, fig_freq = config.fig_time, config.fig_freq

# === Functions ===
def clear_plots():
    print("Cleaning plots")
    fig_time.data = []
    fig_freq.data = []
    plot_time.update()
    plot_freq.update()
    print("Plots cleared")

async def record_audio():
    await asyncio.to_thread(tools.record_audio)

async def play_input():
    await asyncio.to_thread(tools.play_signal, INPUT_FILENAME)

async def play_output():
    await asyncio.to_thread(tools.play_signal, OUTPUT_FILENAME)

async def plot_input():
    await asyncio.to_thread(tools.plot_Input_signal)
    plot_time.update()

async def plot_output():
    await asyncio.to_thread(tools.add_output)
    plot_time.update()

async def generate_output(scale, shift):
    await asyncio.to_thread(sp.time_shift, shift)
    if shift > 0:
        print(f"TIME SHIFTING {shift}")
    await asyncio.to_thread(sp.scaling, scale)
    if scale != 1:
        print(f"SCALING {scale}")
    await asyncio.to_thread(tools.add_output)
    plot_time.update()

async def run_fft():
    print("Running FFT task...")
    freq, magnitude = await asyncio.to_thread(sp.fft, INPUT_FILENAME)
    if freq is None:
        return
    tools.add_fft_trace('FFT Input', INPUT_FILENAME)
    plot_freq.update()
    print("FFT plotted.")

async def apply_filter_dialog(cutoff, btype, dialog, label_prefix):
    try:
        rate, data = tools.open_signal(INPUT_FILENAME)
        filtered = sp.apply_filter(data, rate, cutoff, btype, 5)
        filter_dialog.close()
        tools.save_signal(filtered, rate)
        tools.add_fft_trace(f'{label_prefix} {cutoff} Hz', OUTPUT_FILENAME)
        plot_freq.update()
    except Exception as e:
        print(f"[ERROR] Failed to apply {btype} filter: {e}")
        

# === Unified Filter Dialog ===
filter_dialog = ui.dialog().props('persistent')
filter_slider_single = None
filter_slider_range = None
filter_title_label = None
filter_type = 'highpass'
filter_label_prefix = 'High-Pass'

def update_slider_visibility():
    if filter_type in ['highpass', 'lowpass']:
        filter_slider_single.visible = True
        filter_slider_range.visible = False
        range_min_label.visible = False
        range_min_input.visible = False
        range_max_label.visible = False
        range_max_input.visible = False
        f.visible = True
        f_label.visible = True
        
    else:
        filter_slider_single.visible = False
        filter_slider_range.visible = True
        range_min_label.visible = True
        range_min_input.visible = True
        range_max_label.visible = True
        range_max_input.visible = True
        f_label.visible = False
        f.visible = False
        
    filter_title_label.text = f'{filter_label_prefix} Filter – Cutoff Frequency (Hz)'

def open_filter_dialog(ftype: str, prefix: str):
    global filter_type, filter_label_prefix
    filter_type = ftype
    filter_label_prefix = prefix
    update_slider_visibility()
    filter_dialog.open()
    dropdown_btn.close()

def apply_selected_filter():
    if filter_type in ['highpass', 'lowpass']:
        cutoff = filter_slider_single.value
    else:
        low = model["range"]["min"]
        high = model["range"]["max"]
        print(f"Selected range: {low} - {high}")
        if low >= high:
            ui.notify("[ERROR] Band filter range is invalid. Ensure Min < Max.", type='negative')
            return
        cutoff = (low, high)
    asyncio.create_task(apply_filter_dialog(cutoff, filter_type, filter_dialog, filter_label_prefix))
    
def update_range_slider(min_val: int, max_val: int):
    if filter_slider_range.value != [min_val, max_val]:
        filter_slider_range.set_value([0, 0])  # force redraw
        filter_slider_range.set_value([min_val, max_val])

with filter_dialog:
    with ui.card():
        model = {"range": {"min": 0, "max": 20000}}
        
        filter_title_label = ui.label(f'{filter_label_prefix} Filter \u2013 Cutoff Frequency (Hz)').classes('text-subtitle2 q-mb-md')
        filter_slider_single = ui.slider(min=0, max=20000, value=1000, step=1).props('label-always input')
        filter_slider_range = ui.range(min=model["range"]["min"], max=model["range"]["max"]).bind_value(model, "range").props('label-always input')
        #filter_slider_range = ui.range(min=0, max=20000, value=[1000, 5000], step=1).props('label-always input')
        #filter_slider_range.set_value([1000, 5000])  # explicit init

        with ui.row().classes('items-center justify-between'):
            f_label = ui.label('Cutoff Frequency').classes('text-caption')
            f = ui.number(label='Cutoff Frequency', min=0, max=20000, value=1000, step=1)
        # Two-way binding
        filter_slider_single.bind_value_to(f, 'value')
        filter_slider_single.bind_value_from(f, 'value')
        
        
        with ui.row().classes('items-center justify-between'):
            range_min_label = ui.label('Min Frequency').classes('text-caption')
            range_min_input = ui.number(label='Min Frequency').bind_value(
                model,
                "range",
                backward=lambda x: x["min"],
                forward=lambda x: {"min": x, "max": model["range"]["max"]},
            )
            
        with ui.row().classes('items-center justify-between'):
            range_max_label = ui.label('Max Frequency').classes('text-caption')
            range_max_input = ui.number(label='Max Frequency').bind_value(
                model,
                "range",
                backward=lambda x: x["max"],
                forward=lambda x: {"min": model["range"]["min"], "max": x},
            )

        

        with ui.row().classes('items-center justify-end q-gutter-sm'):
            ui.button('Apply', on_click=apply_selected_filter, icon='check').classes('q-mr-sm')
            ui.button('Close', icon='close', on_click=filter_dialog.close)
            
# === GUI ===
with ui.row().classes('items-center justify-center'):
    ui.image(config.logo).classes('w-20 h-20')
    ui.label('SonicScope').classes('text-h6')

with ui.row().classes('items-start'):
    with ui.column().classes('items-left justify-center q-pa-md gap-4'):
        with ui.tabs() as tabs:
            ui.tab('Input', icon='input')
            ui.tab('Output', icon='output')
            ui.tab('Plot Settings', icon='settings')

        with ui.tab_panels(tabs, value='Input'):
            with ui.tab_panel('Input'):
                with ui.row().classes('items-center justify-center'):
                    ui.label('Input').classes('text-h6')
                with ui.row().classes('items-center justify-center'):
                    ui.button('Record', icon='mic', on_click=lambda: asyncio.create_task(record_audio())).classes('gap-0.5 items-center')
                    ui.button('Play', icon='play_arrow', on_click=lambda: asyncio.create_task(play_input())).classes('gap-0.5 items-center')
                    ui.button('Plot', icon='timeline', on_click=lambda: asyncio.create_task(plot_input())).classes('gap-0.5 items-center')
                '''
                with ui.row().classes('items-center justify-center'):
                    a = ui.audio(INPUT_FILENAME, autoplay=False, controls=True).classes('w-full')
                    a.on('play', lambda _: ui.notify('Playing input'))
                    a.on('ended', lambda _: ui.notify('Completed'))
                '''
                with ui.row().classes('items-center justify-center'):
                    ui.upload(on_upload=tools.upload_signal, label='🎵 Load WAV File')

            with ui.tab_panel('Output'):
                with ui.row().classes('items-left justify-center'):
                    ui.label('Output').classes('text-h6')
                with ui.row().classes('items-center justify-center'):
                    ui.button('Play', icon='play_arrow', on_click=lambda: asyncio.create_task(play_output()))
                    ui.button('Plot', icon='timeline', on_click=lambda: asyncio.create_task(plot_output()))
                    ui.button('Generate', icon='add', on_click=lambda: asyncio.create_task(generate_output(scale_in.value, t_shift_in.value)))
                with ui.row().classes('items-center justify-center'):
                    dropdown_btn = ui.dropdown_button(text='Filters', split=True)
                    with ui.row().classes('items-center justify-center'):
                        with dropdown_btn:
                            ui.item('High-Pass', on_click=lambda: open_filter_dialog('highpass', 'High-Pass'))
                            ui.item('Low-Pass', on_click=lambda: open_filter_dialog('lowpass', 'Low-Pass'))
                            ui.item('Band-Pass', on_click=lambda: open_filter_dialog('bandpass', 'Band-Pass'))
                            ui.item('Band-Stop', on_click=lambda: open_filter_dialog('bandstop', 'Band-Stop'))
                            ui.item('FIR', on_click=lambda: ui.notify('FIR not implemented yet'))
                            ui.item('IIR', on_click=lambda: ui.notify('IIR not implemented yet'))

                        ui.button('FFT', icon='timeline', on_click=lambda: asyncio.create_task(run_fft()))
                with ui.row().classes('items-center justify-center'):
                    scale_in = ui.number(label='Scale', value=1, min=0, max=2, step=0.1)
                    t_shift_in = ui.number(label='Time shifting [ms]', value=0, min=0, step=1)
                
                '''
                with ui.row().classes('items-center justify-center'):
                    a = ui.audio(OUTPUT_FILENAME, autoplay=False, controls=True).classes('w-full')
                    a.on('play', lambda _: ui.notify('Playing output'))
                    a.on('ended', lambda _: ui.notify('Completed'))
                '''
            
            with ui.tab_panel('Plot Settings'):
                with ui.row().classes('items-left justify-center'):
                    ui.label('Plot Settings').classes('text-h6')
                with ui.row().classes('items-center justify-center'):
                    ui.button('Clear Plots', icon='cleaning_services', on_click=clear_plots).classes('gap-0.5 items-center')
                    ui.button('Refresh Plots', icon='refresh', on_click=lambda: (plot_time.update(), plot_freq.update())).classes('gap-0.5 items-center')
                    
    # === Plots ===
    with ui.column().classes('q-pa-md'):
        with ui.tabs() as tabs:
            ui.tab('Time Domain', icon='timeline')
            ui.tab('Frequency Domain', icon='timeline')

        with ui.tab_panels(tabs, value='Time Domain'):
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
                    yaxis_title='Magnitude')
                plot_freq = ui.plotly(fig_freq).classes('w-full h-80')

with ui.footer().classes('items-center justify-center q-pa-none q-mt-none').style('height: 30px;'):
    ui.label('SonicScope – Developed by Ronel Herzass').classes('text-caption q-mb-none').style('line-height: 1; margin: 0; padding: 0')

ui.run()
