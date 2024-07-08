from turtle import color
import numpy as np
from scipy.fftpack import hilbert
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

def filter_delay(num_taps, fs):
    filt_delay = (num_taps - 1) / (2 * fs)
    return filt_delay

def filter_taps(d1=10**-4, d2=10**-3, Df=2000):
    """ https://dsp.stackexchange.com/questions/31066/how-many-taps-does-an-fir-filter-need
    """
    num_taps = int((2/3)*np.log10(1/(10*d1*d2))*Df)
    if not num_taps % 2:
        num_taps += 1
    return num_taps


# Read in signal and noise from file
fs, noise = wavfile.read('noise.wav') # fs == 44100
#fs, stimulus = wavfile.read('dtmf.wav') # fs == 44100
fs, stimulus = wavfile.read('sentence.wav') # fs == 44100
# truncate stimulus to match noise duration
len_noise = len(noise)
dur_noise = len(noise) / fs
#stimulus = stimulus[0:len_noise]
dur_stim = len(stimulus)/ fs

# Calculate time base
t_noise = np.arange(0,dur_noise,1/fs)
t_stim = np.arange(0,dur_stim,1/fs)

# Original stimulus in the time domain
plt.subplot(2,4,1)
plt.plot(t_stim,stimulus)
plt.title('Original stimulus in time')
# Normalized stimulus in the time domain
stimulus_normalized = ts.doNormalize(stimulus)
#stimulus_normalized = stimulus_normalized - np.mean(stimulus_normalized) # Remove DC offset
plt.subplot(2,4,2)
plt.plot(t_stim,stimulus_normalized)
plt.title('Normalized stimulus in time')
# Original noise in the time domain
plt.subplot(2,4,5)
plt.plot(t_noise,noise)
plt.title('Original noise in time')
# Normalized noise in the time domain
noise_normalized = ts.doNormalize(noise)
#noise_normalized = noise_normalized - np.mean(noise_normalized) # Remove DC offset
plt.subplot(2,4,6)
plt.plot(t_noise,noise_normalized)
plt.title('Normalized noise in time')

# Use normalized versions
stimulus = stimulus_normalized
noise = noise_normalized

# FFT of noise and stimulus tones
freqs_noise, fft_noise = ts.doFFT(noise,fs)
freqs_stimulus, fft_stimulus = ts.doFFT(stimulus,fs)

# P Welch of noise and stimulus tones
f_noise, den_noise = signal.welch(noise, fs, nperseg=2048)
f_stimulus, den_stimulus = signal.welch(stimulus, fs, nperseg=2048)
# Plot FFT and P Welch results of noise and stimulus
#fig, axs = plt.subplots(1,2)
#fig.suptitle('FFT and P Welch of noise and stimulus')
# FFT noise
plt.subplot(2,4,7)
plt.plot(freqs_noise,fft_noise)
#plt.plot(fft_noise,10*np.log10(Pxx_noise))
plt.title('FFT Noise')
# FFT stimulus
plt.subplot(2,4,3)
plt.plot(freqs_stimulus,fft_stimulus)
#plt.plot(fft_stimulus,10*np.log10(Pxx_stimulus))
plt.title('FFT Stimulus')
# P Welch noise
plt.subplot(2,4,8)
plt.semilogy(f_noise, den_noise)
plt.title('P Welch Noise')
# P Welch stimulus
plt.subplot(2,4,4)
plt.plot(f_stimulus,den_stimulus)
plt.title('P Welch stimulus')
plt.show()


# Create FIR with shape of stimulus FFT
num_taps = filter_taps()
print(f"Number of taps: {num_taps}")
offset = num_taps - 1

filt_delay = filter_delay(num_taps,fs)
print(f"Filter delay (s): {filt_delay}")

fir_filt = signal.firwin2(numtaps=num_taps, freq=freqs_stimulus/np.max(freqs_stimulus), gain=fft_stimulus)
# Apply FIR to noise
filtered_noise = np.convolve(fir_filt, noise)
# Normalize filtered noise
filtered_noise = filtered_noise / np.max(np.abs(filtered_noise))

# Examine FIR frequency response
w, h = signal.freqz(fir_filt)
w = w * fs / (2*np.pi)
# This is plotted below

# what is this?
#w = w / (2*np.pi)

# Write filtered noise to file
#wavfile.write(file_name, fs, filtered_noise)

# filter shape
plt.subplot(2,3,1)
plt.plot(fir_filt)
plt.title('FIR filter shape')

# FIR frequency response
plt.subplot(2,3,2)
plt.plot(w, 20 * np.log10(abs(h)))
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (dB)")
plt.title("FIR frequency response")

# filtered noise
plt.subplot(2,3,3)
plt.plot(t_noise,filtered_noise[:-offset])
plt.title('Filtered noise')

# Original FFT of stimulus
plt.subplot(2,3,4)
plt.plot(freqs_stimulus,fft_stimulus)
plt.title('Original FFT of stimulus')

# FFT of filtered noise
freqs_filtered_noise, fft_filtered_noise = ts.doFFT(filtered_noise[:-offset],fs)
plt.subplot(2,3,5)
plt.plot(freqs_filtered_noise, fft_filtered_noise)
plt.title('FFT of filtered noise')

# Lowpass filter FFT for visual comparison
env_stimulus = butter_filt(fft_stimulus,'low',50,5,fs)
env_filtered_noise = butter_filt(fft_filtered_noise,'low',50,5,fs)
# Subtract envolopes to show amp differences at each freq
rms_env_stim = ts.rms(env_stimulus)
rms_env_filt_noise = ts.rms(env_filtered_noise)
#amp_diff = env_stimulus/env_filtered_noise
amp_diff = rms_env_filt_noise / rms_env_stim

#plt.subplot(2,3,6)
#plt.plot(freqs_stimulus,20*np.log10(amp_diff))
#plt.plot(freqs_filtered_noise, amp_diff)
#plt.title("Amplitude difference")
plt.show()

plt.subplot(2,1,1)
#plt.plot(freqs_stimulus,20*np.log10(env_stimulus),"blue",label="stimulus")
#plt.plot(freqs_filtered_noise,20*np.log10(env_filtered_noise),"orange",label="Filtered Noise")
plt.plot(freqs_stimulus,env_stimulus,"blue",label="stimulus")
plt.plot(freqs_filtered_noise,env_filtered_noise,"orange",label="Filtered Noise")
plt.title("LPFed stimulus and filtered noise FFT")
plt.legend()

adj_filtered_noise = env_filtered_noise / amp_diff
plt.subplot(2,1,2)
#plt.plot(freqs_stimulus,20*np.log10(env_stimulus),"blue",label="stimulus")
#plt.plot(freqs_filtered_noise,20*np.log10(adj_filtered_noise),":",color="orange",label="Filtered Noise")
plt.plot(freqs_stimulus,env_stimulus,"blue",label="stimulus")
plt.plot(freqs_filtered_noise,adj_filtered_noise,":",color="orange",label="Filtered Noise")
plt.title("Amplitudes after adjustment")
plt.legend()
plt.show()
