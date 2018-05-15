# import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
from scipy.stats import kurtosis, skew
import numpy as np
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
listener = Listener('./audios/wav/mulher_1.wav')
            <listener.Listener object at 0x105ccc350>

        Args:
            file_name (str): The audio file name to get informations.

        Attributes:
            audio_data(array): Receive the audio array data from
                get_audio_data funtion.
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.audio_data = self.get_audio_data()
        self.duration = self.get_duration()
        self.iq1 = np.percentile(self.audio_data, q=25)
        self.iq3 = np.percentile(self.audio_data, q=75)
        self.median = np.percentile(self.audio_data, q=50)
        self.label = 'homem' if 'homem' in file_name else 'mulher'
        self.kurtosis = kurtosis(self.audio_data)
        self.maxfun = np.amax(fft(self.audio_data))
        self.maxfreq = np.amax(self.audio_data)
        self.meanfreq = np.mean(self.audio_data)
        self.meanfun = np.mean(fft(self.audio_data))
        self.minfun = np.amin(fft(self.audio_data))
        self.minfreq = np.amin(self.audio_data)
        self.peak = self.get_peak_frequency()
        self.skew = skew(abs(self.audio_data))
        self.centroid = self.get_centroid()
        self.std = np.std(self.audio_data)

    def get_audio_data(self):
        """Get data from an audio file with .wav extension.

        Args:
            file_name (str): Audio file name.

        Attributes:
            rate(int): Sample rate of wav file.
            data(array): Data read from wav file.

        Return:
            data(array): Data read from wav file.
        """
        rate, data = wav.read(self.file_name)
        return data

    def get_duration(self):
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
        with contextlib.closing(wave.open(self.file_name, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    def get_peak_frequency(self):
        """
        https://stackoverflow.com/questions/37813059/i-am-getting-peak-
        frequency-from-wav-file-but-for-recorded-2-channels-wav-it-is#answer-37855872
        """
        fname = self.file_name
        wav_file = wave.open(fname, 'r')
        self.frate = wav_file.getframerate()
        data_size = wav_file.getnframes()
        data = wav_file.readframes(data_size)
        nChannels = wav_file.getnchannels()
        nSample = wav_file.getsampwidth()
        data_size = data_size * nChannels * nSample
        wav_file.close()
        if nSample == 2:
            fmt = "<i2"
        else:
            fmt = "<i4"
        data = np.frombuffer(data, dtype=fmt)
        if nChannels == 2:
            data = data.reshape(-1, nChannels)
            data = data.sum(axis=1) / 2
        # and now the same way as above as said by maxpowers
        freq_nq = len(data) // 2
        x = abs(np.fft.fft(data))[:freq_nq] / len(data) * 2
        freqs = np.fft.fftfreq(len(data), 1. / self.frate)[:freq_nq]
        return freqs[np.argmax(x)]

    def get_centroid(self):
        """
        Compute the spectral centroid.
        Characterizes the "center of gravity" of the spectrum.
        Approximately related to timbral "brightness"
        """
        binNumber = 0

        numerator = 0
        denominator = 0

        for bin in self.audio_data:
            f = (self.frate / 2.0) / len(self.audio_data)
            f = f * binNumber

            numerator = numerator + (f * abs(bin))
            denominator = denominator + abs(bin)

            binNumber = binNumber + 1

        return (numerator * 1.0) / denominator

    def save_into_csv(self):
        """Function to save information from audio to .csv file

        Args:
            All informations required

        Todo:
            Make this function
        """
        # print(self)
        pass
