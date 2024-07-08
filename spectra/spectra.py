"""Plot spectrograms and FFTs

    Author: Travis M. Moore
    Created: 22 Aug, 2022
    Last Edited: 22 Aug, 2022
"""

###########
# Imports #
###########
# Import data science packages
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
from scipy.fft import rfft, rfftfreq
from scipy import signal

# Import audio packages
import sounddevice as sd

# Import system packages
from pathlib import Path

# Import custom modules
from models import Audio


#############
# Functions #
#############
def doFFT(sig, fs, N=2048):
    """
        Wrapper function for scipy rfft. Calculate 
        a single-sided fast Fourier transform for a 
        given signal SIG and sampling rate FS. For 
        a double-sided FFT (i.e., with negative half 
        from imaginary numbers), use scipy fft function.

            SIG: A 1- or 2-channel signal. Note 
                2-channel signals are first combined.
            FS: sampling rate in Hz

        Based on tutorial: https://realpython.com/python-scipy-fft/
        Adapted by: Travis M. Moore
        Last edited: Feb. 2, 2022
    """
    # Combine channels for 2-channel signals
    if len(sig.shape) == 2:
        combo = sig[0] + sig[1]
        sig = combo / combo.max() # normalize

    yf = rfft(sig, N)
    xf = rfftfreq(N, 1/fs)
    return xf, np.abs(yf)


def butter_filt(sig, type, cutoff, order, fs):
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    b, a = signal.butter(order, norm_cutoff, btype=type, analog=False)
    y = signal.filtfilt(b, a, sig)
    return y


#########
# BEGIN #
#########
# Import data
# Import list of full file paths
path = 'C:\\Users\\MooTra\\Documents\\Code\\Python\\proto\\spectra\\recordings'
files = Path(path).glob('*.wav')

# Get audio objects for selected files
audio_list = []
for file in files:
    a = Audio(str(file), 0)
    #if "Stim1_" in a.name:
        # # Filtering
        # left = butter_filt(a.working_audio[:,0], 'low', 9000, 5, a.fs)
        # right = butter_filt(a.working_audio[:,1], 'low', 9000, 5, a.fs)
        # combo = np.array([left, right]).T
        # a.working_audio = combo

        # left = butter_filt(a.working_audio[:,0], 'high', 120, 5, a.fs)
        # right = butter_filt(a.working_audio[:,1], 'high', 120, 5, a.fs)
        # combo = np.array([left, right]).T
        # a.working_audio = combo

    audio_list.append(a)


# Set style
plt.style.use('seaborn')


# MONO: specify channel
def do_plots_mono(audio_obj, chan=0):
    """Plot time waveform, spectrogram, FFT
    """
    # if ax is None:
    #     ax = plt.gca()

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)

    # Time waveform
    ax1.plot(audio_obj.t, audio_obj.working_audio[:,chan])
    ax1.set(title="Time Waveform", xlabel="Time (s)", ylabel="Amplitude")
    ax1.set_xlim([0, audio_obj.t[-1]])
    ax1.set_ylim([-1, 1])

    # Spectrogram
    Pxx, freqs, bins, im = ax2.specgram(
        audio_obj.working_audio[:,chan],
        NFFT=2048,
        Fs = audio_obj.fs,
        noverlap=900
    )
    ax2.set(title="Spectrogram", xlabel="Time (s)", ylabel="Frequency (Hz)")
    ax2.grid(False)

    # FFT
    xf, yf = doFFT(audio_obj.working_audio[:,chan], audio_obj.fs, N=2048)
    ax3.plot(xf, yf)
    ax3.set(title="FFT", xlabel="Frequency (Hz)", ylabel="Amplitude")

    plt.suptitle(audio_obj.name + f'\nChannel: {chan}')
    #plt.show()
    return fig


# MULTI-CHANNEL: Plot all channels
def do_plots_stereo(audio_obj, chan=0):
    """Plot time waveform, spectrogram, FFT
    """
    chans = ['left', 'right']

    fig, ax = plt.subplots(nrows=3, ncols=audio_obj.channels)

    # Time waveform #
    ax[0,0].plot(audio_obj.t, audio_obj.working_audio[:,0])
    ax[0,1].plot(audio_obj.t, audio_obj.working_audio[:,1])

    for idx, val in enumerate([ax[0,0], ax[0,1]]):
        val.set(title=("Time Waveform: " + chans[idx]), xlabel="Time (s)", ylabel="Amplitude")
        val.set_xlim([0, audio_obj.t[-1]])
        #val.set_ylim([-1, 1])

    # Spectrogram #
    Pxx, freqs, bins, im = ax[1,0].specgram(
        audio_obj.working_audio[:,0],
        NFFT=2048,
        Fs = audio_obj.fs,
        noverlap=900
    )
    Pxx, freqs, bins, im = ax[1,1].specgram(
        audio_obj.working_audio[:,1],
        NFFT=2048,
        Fs = audio_obj.fs,
        noverlap=900
    )

    for idx, val in enumerate([ax[1,0], ax[1,1]]):
        val.set(title=("Spectrogram: "  + chans[idx]), xlabel="Time (s)", ylabel="Frequency (Hz)")
        val.grid(False)

    # FFT #
    xf, yf = doFFT(audio_obj.working_audio[:,0], audio_obj.fs, N=2048)
    ax[2,0].plot(xf, yf)
    xf, yf = doFFT(audio_obj.working_audio[:,1], audio_obj.fs, N=2048)
    ax[2,1].plot(xf, yf)

    for idx, val in enumerate([ax[2,0], ax[2,1]]):
        val.set(title=("FFT: " + chans[idx]), xlabel="Frequency (Hz)", ylabel="Amplitude")

    plt.suptitle(audio_obj.name)
    plt.savefig(audio_obj.name + '.png', dpi=300)
    return plt


# Generate plots
counter = 0
while counter < len(audio_list):
    plt.figure(counter)
    do_plots_stereo(audio_list[counter], chan=0)
    counter += 1

#do_plots_stereo(audio_list[0], chan=0)

#plt.show()

#audio_list[0].play()
