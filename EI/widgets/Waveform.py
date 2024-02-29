# establish audio recording
import io

import cv2
import numpy
import pyaudio
import wave
import librosa
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read, write
from FindMF import extract_main_frequency

WAV_FILE = "/tmp/wavefile.wav"
CHANNEL_NUM = 1

class Waveform:
    contextual_audio_data = None
    timbre = None

    def __init__(self, chunk=1024, channels=1, rate=44100, lossy_simulation=False, mfcc=True):
        self.chunk = chunk
        self.channels = channels
        self.rate = rate
        self.lossy_simulation = lossy_simulation
        self.mfcc = mfcc

    def record(self, seconds=1):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk)
        frames = []
        for i in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAV_FILE, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def extractor(self) -> int:
        if self.contextual_audio_data is not None:
            return self.contextual_audio_data
        self.contextual_audio_data = self.contextual_audio_data[:1024]

        if self.lossy_simulation:
            # simulate loss by smoothening the using gauss convolution
            kernel_size = 128
            kernel = cv2.getGaussianKernel(kernel_size, 0.5)
            kernel = kernel / kernel.sum()
            lossy_audio_2d = cv2.filter2D(self.contextual_audio_data, -1, kernel)
            self.contextual_audio_data = numpy.array(lossy_audio_2d, dtype=numpy.int16)

        # extract the main frequency and calculate window size
        main_frequency = extract_main_frequency(self.contextual_audio_data, self.rate)
        window_size = int(self.rate / main_frequency)
        if self.mfcc:
            self.timbre = librosa.feature.mfcc(y=self.contextual_audio_data, sr=self.rate, n_mfcc=13, hop_length=window_size)
        else:
            self.timbre = self.contextual_audio_data[:window_size]

def start(self):
        self.record()
        rosa_audio_data, sample_rate = librosa.load(WAV_FILE)

        # trim the audio clip to 0.2 s
        self.contextual_audio_data = rosa_audio_data[:int(0.1 * self.rate)]
        self.extractor()

        # plot the waveform
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        ax.plot(self.timbre)
        io_buf = io.BytesIO()
        ax.savefig(io_buf, format='raw', dpi=10)
        io_buf.seek(0)
        show = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                             newshape=(int(ax.bbox.bounds[3]), int(ax.bbox.bounds[2]), -1))
        io_buf.close()

        return show