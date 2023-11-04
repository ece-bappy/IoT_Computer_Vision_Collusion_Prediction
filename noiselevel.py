import pyaudio
import numpy as np
import keyboard  # Import the keyboard library

# Parameters for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

audio = pyaudio.PyAudio()

stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("Real-time noise level monitoring...")

# Initialize an empty list for the audio data
audio_data = []

try:
    while True:
        data = stream.read(CHUNK)
        audio_data.extend(np.frombuffer(data, dtype=np.int16))

        # Keep a fixed buffer size (adjust as needed)
        if len(audio_data) > RATE:
            audio_data = audio_data[-RATE:]

        # Calculate the RMS for the current buffer
        rms = np.sqrt(np.mean(np.array(audio_data) ** 2))

        print(f"Current RMS: {rms:.2f} dB")

        # Check if the "q" key is pressed to stop the loop
        if keyboard.is_pressed("q"):
            break
except KeyboardInterrupt:
    pass
finally:
    # Release resources when done
    stream.stop_stream()
    stream.close()
    audio.terminate()
