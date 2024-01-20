# establish audio recording

import pyaudio
import wave

class Waveform:
    def __init__(self, chunk=1024, channels=1, rate=44100):
        self.chunk = chunk
        self.channels = channels
        self.rate = rate
