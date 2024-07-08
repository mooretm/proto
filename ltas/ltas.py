import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fft import irfft
from matplotlib import pyplot as plt
import sounddevice as sd

import sys


#sys.path.append('.\\lib') # Point to custom library file
sys.path.append('C:\\Users\\MooTra\\Documents\\Code\\Python\\my_packages\\tmpy')
import tmsignals as ts # Custom library
import importlib 
importlib.reload(ts) # Reload custom module on every run

# Prototyping code for LTAS
""" Calculate spectrum of pure tone 
fs = 48000
t, sig = ts.mkTone(1000,0.5)
f, Pxx_den = signal.welch(sig, fs, nperseg=1024)
plt.semilogy(f, Pxx_den)

y = np.where(Pxx_den == Pxx_den.max())
x = f[y]
plt.semilogy(x,Pxx_den.max(),'o')
plt.title('Highest energy at ' + str(x) + ' Hz')
plt.show()
"""

""" Calculate spectrum of pink noise from file
fs, pinknoise = wavfile.read('pinknoise.wav')
plt.plot(pinknoise)
plt.show()
# Compute and plot power spectral density
f, Pxx_den = signal.welch(pinknoise, fs, nperseg=1024)
plt.semilogy(f, Pxx_den)
plt.show()
"""

""" It does NOT work to convolve the spectrum with 
    noise to 'filter' the noise, for example, when 
    making calibration stimuli. There IS a way to 
    do it, but it's not this simple. 
#fs, pinknoise = wavfile.read('pinknoise.wav')
fs, pinknoise = wavfile.read('noise.wav')
pinknoise = np.array(pinknoise,dtype=int)
pinknoise = ts.setRMS(pinknoise,-10)
fs, dtmf = wavfile.read('dtmf.wav')
# Compute and plot power spectral density
f, dtmfPwr = signal.welch(dtmf, fs, nperseg=1024)
plt.semilogy(f, dtmfPwr)
plt.title('Spectrum of DTMF tones')
plt.show()

f, pinkPwr = signal.welch(pinknoise, fs, nperseg=1024)
plt.semilogy(f, pinkPwr)
plt.title('Spectrum of pinknoise')
plt.show()

# fsig = np.convolve(dtmfPwr, pinknoise)
# f2, Pxx_den_Noise2 = signal.welch(fsig, fs, nperseg=1024)
# plt.semilogy(f2, Pxx_den_Noise2)
# plt.title('Spectrum of filtered pinknoise')
# plt.show()


#fsig = dtmfPwr * pinkPwr
fsig = np.convolve(dtmfPwr, pinkPwr)
f2, Pxx_den_Noise2 = signal.welch(fsig, fs, nperseg=1024)
plt.semilogy(f2, Pxx_den_Noise2)
plt.title('Spectrum of filtered pinknoise')
plt.show()

"""





# Read in noise and dtmf tones from file
fs, noise = wavfile.read('noise.wav') # fs == 44100
fs, dtmf = wavfile.read('dtmf.wav') # fs == 44100
fs, dtmf = wavfile.read('sentence.wav') # fs == 44100
#print('len noise: %f' % len(noise))
#print('len dtmf: %f' % len(dtmf))
# Truncate noise to fit dtmf length
#len_dtmf = len(dtmf)
#noise = noise[0:len_dtmf]
# Truncate sentence to fit noise
len_noise = len(noise)
dur = len(noise) / fs
dtmf = dtmf[0:len_noise]

# Remove DC offset
noise = noise - np.mean(noise)
dtmf = dtmf - np.mean(dtmf)

# Calculate time base
t = np.arange(0,dur,1/fs)

# FFT of noise and dtmf tones
freqs_noise, fft_noise = ts.doFFT(noise,fs)
freqs_dtmf, fft_dtmf = ts.doFFT(dtmf,fs)


"""
# Square to calculate power?
fft_noise = fft_noise**2
fft_dtmf = fft_dtmf**2
# Divide FFT by fs to calculate spectral density?
fft_noise = fft_noise[1:len(fft_noise)-1] / fs
fft_dtmf = fft_dtmf[1:len(fft_dtmf)-1] / fs

# MATLAB junk from: https://www.mathworks.com/matlabcentral/answers/33653-psd-estimation-fft-vs-welch
nfft = len(noise)
fft_noise = np.abs(fft_noise)**2
fft_dtmf = np.abs(fft_dtmf)**2
NumUniquePts = int(nfft/2+1)
fft_noise = fft_noise[0:NumUniquePts]
fft_dtmf = fft_dtmf[0:NumUniquePts]
fft_noise[1:len(fft_noise)-1] = fft_noise[1:len(fft_noise)-1]*2
fft_dtmf[1:len(fft_dtmf)-1] = fft_dtmf[1:len(fft_dtmf)-1]*2
Pxx_noise = fft_noise/fs
Pxx_dtmf = fft_dtmf/fs
fft_noise = np.arange(0,NumUniquePts)*fs/nfft; 
fft_dtmf = np.arange(0,NumUniquePts)*fs/nfft; 
"""


# P Welch of noise and dtmf tones
f_noise, den_noise = signal.welch(noise, fs, nperseg=1024)
f_dtmf, den_dtmf = signal.welch(dtmf, fs, nperseg=1024)
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

# Multiply FFT of noise and dtmf
filt_fft = fft_noise * fft_dtmf
filt_fft = filt_fft - np.mean(filt_fft) # remove DC offset
# Return to time domain
ifft_filt_fft = irfft(filt_fft)
ifft_filt_fft = ifft_filt_fft - np.mean(ifft_filt_fft)
# Set RMS level
ifft_sig = ts.setRMS(ifft_filt_fft,-20)
ifft_sig = ifft_sig - np.mean(ifft_sig)


# Multiplied FFTs (shaped noise) in frequency domain
plt.subplot(2,2,1)
plt.plot(freqs_noise, filt_fft)
plt.title('fft_noise * fft_dtmf')
# Multiplied FFTs (shaped noise) in time domain
plt.subplot(2,2,2)
#plt.plot(ifft_sig[5000:len(ifft_sig)-5000])
plt.plot(ifft_sig)
plt.title('IFFT')
# Original FFT of dtmf tones
plt.subplot(2,2,3)
plt.plot(freqs_dtmf,fft_dtmf)
plt.title('Original FFT of DTMF')
# Original dtmf in the time domain
plt.subplot(2,2,4)
plt.plot(t,dtmf)
plt.title('Original DTMF in time')
plt.show()

# Does the ifft of the original fft_dtmf look right in time?
ifft_dtmf = irfft(fft_dtmf)
plt.plot(t,ifft_dtmf)
plt.show()



"""
sd.play(noise,fs)
sd.wait(2)
sd.play(dtmf,fs)
sd.wait(2)
sd.play(ifft_sig,fs)
sd.wait(2)
"""

