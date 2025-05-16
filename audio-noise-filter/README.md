# 🔇 Real-Time Audio Noise Filter App

An interactive Python-based GUI tool for recording, processing, visualizing, and playing audio signals—designed for real-time signal processing, experimentation, and learning.

## 🚀 Features

- 🔴 **Record** audio from your microphone (stereo, 5 seconds)
- ▶️ **Play** both raw and processed audio
- 📈 **Plot** input and output waveforms using Plotly
- 📤 **Upload** WAV files for analysis
- ⚙️ **Apply transformations** like:
  - Amplitude **scaling**
  - Time-domain **shifting**
  - Basic **FFT** visualization (upcoming)
- 🎚️ **Filter menu** interface (upcoming):
  - High-Pass, Low-Pass, Band-Pass, Band-Stop
  - FIR and IIR filter types
- ✨ Built with **NiceGUI** for interactive web UI

## 🐍 Python Version

Tested with **Python 3.10+**

## 📦 Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## ▶️ Running the App

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt

2. **Start the app**:

    ```bash
    python gui.py

3. **Open in your browser**:

    Visit <http://localhost:8080> to use the web-based interface.

## 📂 File Structure

```bash
audio-noise-filter/
├── assets/
│   ├── input.wav         # Recorded input audio
│   └── output.wav        # Processed output audio
├── gui.py                # NiceGUI frontend and layout
├── signal_tools.py       # Audio handling: record, play, upload, plot
├── signal_processing.py  # Signal processing: scaling, shifting, FFT
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 📚 Lessons Learned

While developing the app, I learned that `scipy.io.wavfile.read()` returns a NumPy array where stereo audio has shape `(samples, 2)`. Using `np.fromstring()` on this array incorrectly flattened it, causing slow-motion playback and incorrect signal length. The fix was to use one channel via `data = data[:, 0]` and avoid reinterpreting the array.  

More on this topic: [SciPy WAV file documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html)

## 🔍 Filtering Logic (Planned)

The app provides a dropdown menu for common digital filter types, which are currently placeholders. Future updates will include:

- **Time-domain filtering** using convolution
- **Frequency-domain filtering** using FFT
- Parameter controls for cutoff frequency, gain, etc.

## 📄 License

This project is licensed under the MIT License.
