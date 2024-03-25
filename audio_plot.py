# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 09:14:36 2024

@author: khoa
"""

import matplotlib.pyplot as plt
import numpy as np
import wave
from scipy.signal import find_peaks
from scipy import signal

spf = wave.open(r"C:\Users\khoac\Downloads\audio2.wav")

# Extract Raw Audio from Wav File
y = spf.readframes(-1)
y = np.fromstring(y, "int16")
peaks, _ = find_peaks(y, height=20000)
frames = spf.getnframes()
rate = spf.getframerate()
duration = frames / float(rate)
for i in range (0,len(peaks)):
    print("peak of y 1 at: ",peaks[i]/rate)
    
delay_seconds = 0.9124 # seconds
delay_samples = int(delay_seconds * rate)
delayed_y = np.concatenate((np.zeros(delay_samples), y))
peaks_2, _ = find_peaks(delayed_y, height=20000)
for i in range (0,len(peaks_2)):
    print("peak of y 2 at: ",peaks_2[i]/rate)
    


correlation = signal.correlate(delayed_y, y, mode="full")
lags = signal.correlation_lags(delayed_y.size, y.size, mode="full")
lag = lags[np.argmax(correlation)]
print(lag/rate)

plt.figure(1)
plt.title("y Wave...")
plt.plot(y)
plt.plot(delayed_y)
plt.plot(peaks, y[peaks],"o")
plt.plot(peaks_2, delayed_y[peaks_2],"o")
plt.show()






