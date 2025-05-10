# 🔇 Real-Time Audio Noise Filter App

An interactive Python-based GUI tool for recording, playing, visualizing, and filtering audio signals—designed for learning, experimentation, and real-time signal processing.

---

## 🚀 Features

- 🔴 **Record** audio from your microphone
- ▶️ **Play** back the recording instantly
- 🎵 **Upload** any WAV file to analyze or clean
- 📈 **Visualize** waveforms using Plotly
- ✨ Built with **NiceGUI** for a responsive user interface
- 🧼 Future support for **real-time denoising** and frequency-domain filtering

---

## 🐍 Python Version

Tested with **Python 3.10+**

---

## 📦 Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📂 File Structure

- `gui.py`: Main GUI layout and interactions
- `audio_tools.py`: Audio handling functions—record, play, upload, plot and fillter
- `assets/`: Logo and static assets

### 🔍 Filtering Logic (Coming Soon)

The filtering module will allow applying **digital filters** (e.g., low-pass, high-pass, band-stop) to clean unwanted noise from audio signals. This will be done using either:

- **Time-domain convolution** with custom filter kernels, or
- **Frequency-domain filtering** using the Fast Fourier Transform (FFT), where specific frequency bands are attenuated or removed.

The goal is to give users an intuitive way to clean recordings and understand how filters affect real-world signals—bridging theoretical DSP concepts with practical audio effects.
