# 🔊 SonicScope – Real-Time Audio Signal Visualizer & Editor

An interactive Python GUI app to **record**, **analyze**, and **manipulate** audio signals in real-time. Built with [NiceGUI](https://nicegui.io), this tool provides an educational and exploratory environment for working with digital signals in both time and frequency domains.

## 🚀 Features

- 🎙 **Record** stereo audio (5 seconds) from your microphone
- 🔁 **Play** both input and output WAV signals
- 📈 **Visualize** signals in:
  - Time domain
  - Frequency domain (via **FFT**)
- 📤 **Upload** and analyze custom WAV files
- ✨ **Transform** your signal with:
  - Amplitude **scaling**
  - Time-domain **shifting** (support in progress)
- 🧹 **Clear** and refresh plots interactively
- 🎛️ **Apply Filters** using a unified dialog:
  - High-Pass, Low-Pass, Band-Pass, Band-Stop
  - Interactive sliders for single and range cutoffs
  - Support for **Butterworth filters** (FIR & IIR support in progress)
- 🧩 **Modular architecture**:
  - `signal_tools.py` for I/O and plotting
  - `signal_processing.py` for DSP logic
  - `gui.py` for UI using NiceGUI
  - `config.py` for centralized configuration

## 🖼️ Demo

![Demo of the app in action](assets/demo.gif)

## 🐍 Python Version

- Requires **Python 3.10+**

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/rh8991/signal-processing-roadmap.git
   cd signal-processing-roadmap/SonicScope
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:

   ```bash
   python gui.py
   ```

4. **Open in browser**:

   Visit [http://localhost:8080](http://localhost:8080)

## 📂 File Structure

```
SonicScope/
├── assets/                # System files (input/output WAV, logo, samples)
│   ├── input.wav
│   ├── output.wav
│   ├── ANF_logo.png
│   ├── demo.gif
│   └── samples/
│       ├── sine_440.wav
│       └── sine_120.wav
├── config.py              # Shared constants and plot initialization
├── gui.py                 # NiceGUI front-end layout and interaction logic
├── signal_tools.py        # Signal utilities: record, play, upload, plot
├── signal_processing.py   # DSP functions: FFT, filters, scaling, shifting
├── requirements.txt       # Project dependencies
└── README.md              # This file
```

## 📚 Lessons Learned

While building this project, I discovered key differences in how stereo audio is handled in NumPy arrays and SciPy WAV readers. Flattening stereo channels using `np.fromstring()` led to **incorrect playback speed** and signal length. The fix involved **selecting one audio channel (`data[:, 0]`)** and ensuring memory contiguity using `np.ascontiguousarray()`.

🧠 Want to understand this better? Read more in the [SciPy WAV documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html)

## 🤝 Contributing

Contributions are welcome!

- Fork the repo and open a PR
- Report issues or suggest features
- ⭐ Star the project to support it!

GitHub: [https://github.com/rh8991/signal-processing-roadmap](https://github.com/rh8991/signal-processing-roadmap)

## 📄 License

MIT License – free to use, modify, and distribute.
