import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

sample_rate = 44100  # Sample rate in Hz
duration = 5  # Duration in seconds
filename = "audio-noise-filter/output.wav"  # Output filename

recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
sd.wait()  # Wait until recording is finished

print("Recording finished.")
print("Saving to file...")
print (recording)
write(filename, sample_rate, recording)  # Save as WAV file
