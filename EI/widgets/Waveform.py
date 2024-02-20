# establish audio recording
import io

import pyaudio
import wave
import librosa
import matplotlib.pyplot as plt
import numpy as np

wav_file = "/tmp/wavefile.wav"

class Waveform:
    def __init__(self, chunk=1024, channels=1, rate=44100):
        self.chunk = chunk
        self.channels = channels
        self.rate = rate

    def record(self, seconds=1):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk)
        print("* recording")
        frames = []
        for i in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(wav_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def start(self):
        rosa_audio_data, sample_rate = librosa.load(wav_file)

        # trim the audio clip to 0.2 s
        rosa_audio_data = rosa_audio_data[:int(0.1 * self.rate)]

        # plot the waveform
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        ax.plot(rosa_audio_data)

        io_buf = io.BytesIO()
        ax.savefig(io_buf, format='raw', dpi=10)
        io_buf.seek(0)
        show = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                             newshape=(int(ax.bbox.bounds[3]), int(ax.bbox.bounds[2]), -1))
        io_buf.close()

        return show