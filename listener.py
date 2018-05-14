# import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
# import numpy as np
import wave
import contextlib


class Listener(object):
    """Get essencial informations from an audio file and save into CSV file.

        Note:
            It is taking so much time to calculate the mode
            >>> self.mode = mode(self.audio_data)
            ModeResult(mode=array([[-29, -29]],
                       dtype=int16),
                       count=array([[2074, 2074]]))

        Example:
            from listener import Listener
            listener = Listener('./audios/wav/mulher_8.wav')
            <listener.Listener object at 0x105ccc350>

        Args:
            file_name (str): The audio file name to get informations.

        Attributes:
            audio_data(array): Receive the audio array data from
                get_audio_data funtion.
    """
    def __init__(self, file_name):
        self.audio_data = self.get_audio_data(file_name)  # file name example
        self.duration = self.get_duration(file_name)
        self.iq1 = self.audio_data[int(0.25 * len(self.audio_data))]
        self.iq3 = self.audio_data[int(0.75 * len(self.audio_data))]
        self.label = 'homem' if 'homem' in file_name else 'mulher'
        self.maxfun = fft(self.audio_data).max()
        self.maxfun = self.audio_data.max()
        self.meanfreq = self.get_mean_frequency(self.audio_data)
        self.meanfun = self.get_mean_fundamental_frequency(self.audio_data)
        self.minfun = fft(self.audio_data).min()
        self.minfreq = self.audio_data.min()

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

    def get_mean_frequency(self, audio_data):
        """Get the mean of audio frequency in Hz

        Args:
            audio_data(array): Data read from wav file

        Return:
            Average from data read from wav file
        """
        return sum(audio_data) / len(audio_data)

    def get_mean_fundamental_frequency(self, audio_data):
        """Get the mean of audio fundamental frequency in Hz

        Args:
            audio_data(array): Data read from wav file

        Return:
            Average from fundamental frequency

        Todo:
            Verify if it is correct.
        """
        return sum(fft(audio_data)) / len(fft(audio_data))

    def save_into_csv(self):
        """Function to save information from audio to .csv file

        Args:
            All informations required

        Todo:
            Make this function
        """
        pass
