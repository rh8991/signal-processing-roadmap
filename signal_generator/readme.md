# 🎶 Signal Generator Simulation in Python

This is a simple, interactive signal generator built in Python. It allows you to generate, visualize, and play audio signals like sine, square, triangle, and sawtooth waves with custom frequency, amplitude, duration, phase, and offset.

---

## 🚀 Features

- 📀 Generate basic signals: **Sine**, **Square**, **Triangle**, and **Sawtooth** (more coming soon)
- 🎛 Set frequency, amplitude, duration, **phase**, and **offset**
- 📊 Visualize waveforms using Matplotlib
- 🔊 Play signals as audio
- 🖼 GUI built with PySimpleGUI (Windows-friendly)

---

## 📦 Requirements

Install the dependencies using pip:

```bash
pip install numpy matplotlib sounddevice PySimpleGUI
```

---

## 🧠 Signal Types & Descriptions

- **Sine Wave**: A smooth periodic oscillation
- **Square Wave**: Alternates between max and min amplitude (on/off)
- **Triangle Wave**: Linearly rises and falls symmetrically
- **Sawtooth Wave**: Linearly rises then drops sharply

---

## 💻 How It Works

The app uses a GUI to let you configure signal properties, plot the waveform, and optionally play it as sound. Ideal for education, audio testing, or signal processing experiments.

---

## 🛠 Usage Example

```python
from signals import generate_sine

fs = 44100
freq = 440
amp = 1.0
phase = 0
offset = 0
duration = 1.0

# Generate a sine wave
t, y = generate_sine(freq, amp, phase, offset, duration, fs)
```

---

## 📂 File Structure

- `main.py`: Launches GUI and handles user interactions
- `signals.py`: Signal generation functions
- `gui.py`: Builds the GUI interface
- `plotter.py`: Plots signal using matplotlib
- `player.py`: Plays signal using sounddevice

---

## 📣 Coming Soon

- Custom signal editor
- White/pink noise generator
- Export signal to WAV/CSV
- Real-time signal playback

---

Made with 💻 and 🎷
