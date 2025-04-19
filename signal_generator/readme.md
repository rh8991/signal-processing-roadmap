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
🔍 Bonus: Human Hearing and Digital Signals

While building this Signal Generator, I wanted to go beyond just visualizing waveforms—I wanted to hear them too. This opens the door to a fascinating intersection between digital signal processing and human perception.

Humans can typically hear frequencies from 20 Hz to 20,000 Hz, though the upper limit decreases with age. Our ears don't just "hear" frequency—they interpret complex patterns of amplitude, phase, and harmonic content. That’s why a square wave sounds harsh and a sine wave sounds smooth, even if they have the same frequency.

But here’s the twist: computers don’t hear—they only deal with numbers. When we generate a signal in Python or MATLAB, we're discretizing it into samples using a sampling rate (e.g., 44,100 samples/sec). According to the Nyquist Theorem, to accurately reproduce a signal, we must sample at least twice its highest frequency. Fail to do this, and we get aliasing, where signals appear as lower frequencies than they really are—an audio illusion of sorts.

Once the signal is sampled and converted to digital data, it’s passed through the sound card’s digital-to-analog converter (DAC), then finally reproduced by your headphones or speakers as vibrations in air. Those vibrations are detected by your ears and interpreted by your brain—completing a beautiful loop from code to cognition.

This part of the project helped me appreciate how the theory I study in class—Nyquist rate, Fourier analysis, anti-aliasing filters—has a real impact on how we experience sound in everyday life.

---
Made with 💻 and 🎷
