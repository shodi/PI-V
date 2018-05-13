import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import wave
import contextlib


class Listener(object):
    """Get essencial informations from an audio file and save into CSV file.

        Example:
            >>> from listener import Listener
            >>> listener = Listener('./audios/wav/mulher_8.wav')
            <listener.Listener object at 0x105ccc350>

        Args:
            file_name (str): The audio file name to get informations.

        Attributes:
            audio_data(array): Receive the audio array data from
                get_audio_data funtion.
    """
    def __init__(self, file_name):
        self.label = 'homem' if 'homem' in file_name else 'mulher'
        self.duration = self.get_duration(file_name)
        self.audio_data = self.get_audio_data(file_name)  # file name example
        self.mean = self.get_mean(self.audio_data)

    def get_audio_data(self, file_name):
        """Get data from an audio file with .wav extension.

        Args:
            file_name (str): Audio file name.

        Attributes:
            rate(int): Sample rate of wav file.
            data(array): Data read from wav file.

        Return:
            data(array): Data read from wav file.
        """
        rate, data = wav.read(file_name)
        return data

    def get_mean(self, audio_data):
        """Get the mean of audio data in Hz

        Args:
            audio_data(array): Data read from wav file

        Return:
            Average from data read from wav file
        """
        return sum(audio_data) / len(audio_data)

    def get_duration(self, file_name):
        """Get the duration of audio in seconds

        Args:
            file name(str): Audio file name.

        Attributes:
            frames(int): Number of audio frames.
            rate(int): Sampling frequency.
            duration(float): Data read from wav file.

        Return:
            Duration of audio file in seconds
        """
        with contextlib.closing(wave.open(file_name, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration


'''fft_out = fft(data)
import pdb; pdb.set_trace()
print(fft_out)
plt.plot(np.abs(fft_out))
# plt.plot(data)
plt.show()'''
