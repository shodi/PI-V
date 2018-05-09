'''import alsaaudio, time, audioop
import matplotlib.pyplot as plt
import struct
import numpy as np

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)

CHUNCK = 160
BYTE = 4
# Set attributes: Dual, 44100 Hz, 16 bit little endian samples
inp.setchannels(2)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(CHUNCK)

fig, ax = plt.subplots()

x = np.arange(0, BYTE * CHUNCK, 1)
line, = ax.plot(x, np.random.rand(BYTE * CHUNCK))
ax.set_ylim(0, 255)
ax.set_xlim(0, CHUNCK)
while True:
    # Read data from device
    length, data = inp.read()
    if length:
        # Return the maximum of the absolute value of all samples in a fragment.
        # print(audioop.max(data, 2))
        data_int = np.fromstring(data, dtype='b')
        # data_int = np.array(struct.unpack(str(BYTE * CHUNCK) + 'B', data), dtype='b')
        line.set_ydata(data_int)
        fig.canvas.draw()
        fig.canvas.flush_events()
    time.sleep(.001)'''

import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
rate, data = wav.read('./audios/wav/mulher_2.wav')
plt.plot(data)
plt.show()
