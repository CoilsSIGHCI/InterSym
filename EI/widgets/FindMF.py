import math

import librosa
import numpy as np


def extract_main_frequency(audio_data, sample_rate=44100):
    """Extracts the main frequency of an audio spectrum using the numpy library.

    Args:
      audio_data: A numpy array representing the audio spectrum.

    Returns:
      A float representing the main frequency in Hertz.
    """

    audio_spectrum = np.fft.fft(audio_data)

    # Find the index of the maximum amplitude in the audio spectrum.
    max_index = np.argmax(audio_spectrum)

    # Convert the index to frequency in Hertz.
    main_frequency = max_index * sample_rate / len(audio_spectrum)

    return math.ceil(main_frequency)


if __name__ == '__main__':
    # Load the audio file.
    audio_data, sample_rate = librosa.load('wavefile.wav')

    # Extract the main frequency of the audio spectrum.
    main_frequency = extract_main_frequency(audio_data, int(sample_rate))

    # Print the main frequency.
    print('Main frequency:', main_frequency)
