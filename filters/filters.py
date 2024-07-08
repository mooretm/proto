import numpy as np
from scipy.io import wavfile
from scipy import signal
from matplotlib import pyplot as plt

from tmpy import tmsignals as ts
import importlib
importlib.reload(ts)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    #y = signal.lfilter(b, a, data)
    y = signal.filtfilt(b, a, data)
    return y

def butter_filt(sig, type, cutoff, order, fs=48000):
    if type == 'low' or type == 'high':
        nyq = 0.5 * fs
        norm_cutoff = cutoff / nyq
        b, a = signal.butter(order, norm_cutoff, btype=type, analog=False)
        y = signal.filtfilt(b, a, sig)
        return y


        



""" Filter sawtooth wave
#sig = ts.mkNoise(np.arange(100,4000,10),0.5,48000)
harms = np.arange(2,60,2)
amps = [1/x for x in harms]
phis = np.zeros(len(harms),dtype=int)
t, sig = ts.addSynth(1,harms,amps,phis,0.2,48000)

y = butter_lowpass_filter(sig,30,48000,5)

plt.plot(sig, 'b-', label='data')
plt.plot(y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show()
"""

""" Filter out noise """
t, sig500 = ts.mkTone(500,0.2)
t, sig4000 = ts.mkTone(4000,0.2)
combo = sig500 + sig4000
combo = combo / combo.max()
y = butter_lowpass_filter(combo,700,48000,5)
plt.plot(combo, 'b-', label='Original')
plt.plot(y, 'g-', linewidth=3, label='Filtered')
plt.xlim([0,1/500*48000*4])
plt.xlabel('Time')
plt.grid()
plt.legend()
plt.show()


""" Show mkITD2 envelope using Hilbert transform 
sig = ts.mkITD(500,0.05,-800,0,0.02,48000)
analytic_signal_left = signal.hilbert(sig[0])
amplitude_envelope_left = np.abs(analytic_signal_left)
analytic_signal_right = signal.hilbert(sig[1])
amplitude_envelope_right = np.abs(analytic_signal_right)
plt.plot(sig[0],color='blue')
plt.plot(amplitude_envelope_left,color='blue')
plt.plot(sig[1],color='red')
plt.plot(amplitude_envelope_right,color='red')
plt.xlim([0,1/500*48000*10])
plt.title('Whole waveform shift in time')
plt.show()
"""

"""
# Find envelope of speech signal
#fs = 48000
#sig = ts.mkNoise(np.arange(1,5000,10),0.2,48000)
fs, sig = wavfile.read('sentence.wav')
plt.plot(sig)
plt.title('Original Signal')
plt.show()
# Bandpass filter signal
hpsig = butter_filt(sig,'high',80,5,fs)
bp = butter_filt(hpsig,'low',2500,5,fs)
plt.plot(bp)
plt.title('Bandpass Signal')
plt.show()
# MATLAB web page advice for finding envelope with lpf
#sig2 = sig**2
#sig2 = sig2 * 2
#sig2 = np.sqrt(sig2)
# Full wave rectification
sig2 = np.abs(bp)
plt.plot(sig2)
plt.title('Rectified Signal')
plt.show()
# Find envelope with lpf
y = butter_filt(sig2,'low',25,5,48000)
plt.plot(sig,label='Original')
plt.plot(y,label='LPF')
plt.legend()
plt.show()
# Find envelope with ht
ht = np.abs(signal.hilbert(sig))
plt.plot(sig,label='Original')
plt.plot(ht,label='Hilbert')
plt.legend()
plt.show()
"""


""" Demodulation with LPF 
t, sig50 = ts.mkTone(50,0.05)
t, sig8000 = ts.mkTone(8000,0.05)
ampmod = sig50 * sig8000
plt.plot(t,ampmod)
plt.title('8000-Hz Carrier with 50-Hz Modulator')
plt.show()
# Full wave rectification
ampmod2 = np.abs(ampmod)
plt.plot(ampmod2)
plt.title('Full-Wave Rectified Signal')
plt.show()
# Find envelope with lpf
y = butter_filt(ampmod2,'low',1000,5,48000)
plt.plot(ampmod,label='Original')
plt.plot(y,label='LPF')
plt.legend()
plt.show()
# Find envelope with ht
ht = np.abs(signal.hilbert(ampmod))
plt.plot(ampmod,label='Original')
plt.plot(ht,label='Hilbert')
plt.legend()
plt.show()
"""
