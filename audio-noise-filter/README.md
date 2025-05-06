# Audio Noise Filter (WIP)

This project is an audio recording and processing tool built in Python.  
It uses the `sounddevice` library to capture stereo audio from the microphone and save it as a `.wav` file.

The recorded audio is currently saved in a normalized floating-point format and can be used for further processing, such as filtering noise or analyzing sound features.

> **Status**: This project is a work in progress. More features such as noise filtering, playback, and waveform visualization are planned.

---

## 🐍 Python Version

Tested with **Python 3.10+**. Other versions may work, but are not guaranteed.

---
## Requirements

- Python 3.x  
- `sounddevice`  
- `scipy`  
- `wavio` (optional)

```bash
pip install -r requirements.txt
```