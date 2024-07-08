import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fft import irfft
from matplotlib import pyplot as plt
import sounddevice as sd
import sys
#sys.path.append('.\\lib') # Point to custom library file
sys.path.append('C:\\Users\\MooTra\\Documents\\Code\\Python\\my_packages\\tmpy')
import tmsignals as ts # Custom package
import importlib 
importlib.reload(ts) # Reload custom module on every run


# Read in noise and dtmf tones from file
fs, noise = wavfile.read('noise.wav') # fs == 44100
fs, dtmf = wavfile.read('dtmf.wav') # fs == 44100
fs, dtmf = wavfile.read('sentence.wav') # fs == 44100
# truncate dtmf to match noise duration
len_noise = len(noise)
dur = len(noise) / fs
dtmf = dtmf[0:len_noise]

# Calculate time base
t = np.arange(0,dur,1/fs)

# Original dtmf in the time domain
plt.subplot(2,2,1)
plt.plot(t,dtmf)
plt.title('Original DTMF in time')
# Normalized dtmf in the time domain
dtmf_normalized = ts.doNormalize(dtmf)
#dtmf_normalized = dtmf_normalized - np.mean(dtmf_normalized) # Remove DC offset
plt.subplot(2,2,2)
plt.plot(t,dtmf_normalized)
plt.title('Normalized DTMF in time')
# Original noise in the time domain
plt.subplot(2,2,3)
plt.plot(t,noise)
plt.title('Original noise in time')
# Normalized noise in the time domain
noise_normalized = ts.doNormalize(noise)
#noise_normalized = noise_normalized - np.mean(noise_normalized) # Remove DC offset
plt.subplot(2,2,4)
plt.plot(t,noise_normalized)
plt.title('Normalized noise in time')
plt.show()

# Use normalized versions
dtmf = dtmf_normalized
noise = noise_normalized

# FFT of noise and dtmf tones
freqs_noise, fft_noise = ts.doFFT(noise,fs)
freqs_dtmf, fft_dtmf = ts.doFFT(dtmf,fs)

# P Welch of noise and dtmf tones
f_noise, den_noise = signal.welch(noise, fs, nperseg=2048)
f_dtmf, den_dtmf = signal.welch(dtmf, fs, nperseg=2048)
# Plot FFT and P Welch results of noise and dtmf
fig, axs = plt.subplots(1,2)
fig.suptitle('FFT and P Welch of noise and dtmf tones')
# FFT noise
plt.subplot(2,2,1)
plt.plot(freqs_noise,fft_noise)
#plt.plot(fft_noise,10*np.log10(Pxx_noise))
plt.title('Noise FFT')
# FFT dtmf
plt.subplot(2,2,2)
plt.plot(freqs_dtmf,fft_dtmf)
#plt.plot(fft_dtmf,10*np.log10(Pxx_dtmf))
plt.title('FFT DTMF')
# P Welch noise
plt.subplot(2,2,3)
plt.semilogy(f_noise, den_noise)
plt.title('P Welch Noise')
# P Welch DTMF
plt.subplot(2,2,4)
plt.plot(f_dtmf,den_dtmf)
plt.title('P Welch DTMF')
plt.show()


numtaps = 401
offset = numtaps - 1
#fir_filt = signal.firls(numtaps=201, bands=freqs_dtmf, desired=fft_dtmf)
fir_filt = signal.firwin2(numtaps=numtaps, freq=freqs_dtmf/np.max(freqs_dtmf), gain=fft_dtmf)
filtered_noise = np.convolve(fir_filt, noise)

# Write filtered noise to file
#wavfile.write(file_name, fs, filtered_noise)

# filter shape
plt.subplot(2,2,1)
plt.plot(fir_filt)
plt.title('FIR filter shape')

# filtered noise
plt.subplot(2,2,2)
plt.plot(t,filtered_noise[:-offset])
plt.title('Filtered noise')

# Original FFT of dtmf tones
plt.subplot(2,2,3)
plt.plot(freqs_dtmf,fft_dtmf)
plt.title('Original FFT of DTMF')

# FFT of filtered noise
freqs_noise, fft_noise = ts.doFFT(filtered_noise,fs)
plt.subplot(2,2,4)
plt.plot(freqs_noise, fft_noise)
plt.title('FFT of filtered noise')
plt.show()
