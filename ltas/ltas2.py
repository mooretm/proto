import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fft import irfft
from matplotlib import pyplot as plt
import sounddevice as sd
import random

import sys

#sys.path.append('.\\lib') # Point to custom library file
sys.path.append('C:\\Users\\MooTra\\Documents\\Code\\Python\\my_packages\\tmpy')
import tmsignals as ts # Custom library
import importlib 
importlib.reload(ts) # Reload custom module on every run


def mk_wgn():
    fs = 44100
    dur=3
    random.seed(4)
    wgn = [random.gauss(0.0, 1.0) for i in range(fs*dur)]
    #wgn = ts.doNormalize(wgn)
    #wgn = ts.setRMS(wgn,-30)
    wgn = wgn - np.mean(wgn) # Remove DC offset
    return wgn




fs, dtmf = wavfile.read('dtmf.wav')
#dtmf = ts.doNormalize(dtmf)
#dtmf = ts.setRMS(dtmf,-30)
#dtmf = dtmf - np.mean(dtmf)
# Compute and plot power spectral density
f, dtmfPwr = signal.welch(dtmf, fs, nperseg=1024)
plt.subplot(2,2,1)
plt.semilogy(f, dtmfPwr)
plt.title('Spectrum of DTMF tones')
#plt.show()


dur=3
random.seed(4)
wgn = [random.gauss(0.0, 1.0) for i in range(fs*dur)]
wgn = wgn - np.mean(wgn)

f, noisePwr = signal.welch(wgn, fs, nperseg=1024)
plt.subplot(2,2,2)
plt.semilogy(f, noisePwr)
plt.title('Spectrum of noise')
#plt.show()


fsig = dtmfPwr * noisePwr
#fsig = np.convolve(dtmfPwr, noise)
#fsig = np.convolve(dtmfPwr, noisePwr)
f2, Pxx_den_Noise2 = signal.welch(fsig, fs, nperseg=1024)
plt.subplot(2,2,3)
plt.semilogy(f2, Pxx_den_Noise2)
plt.title('Spectrum of filtered noise')
plt.show()

