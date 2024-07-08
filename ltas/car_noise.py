import scipy
from scipy.io import wavfile
import sys
sys.path.append('C:\\Users\\MooTra\\Documents\\Code\\Python\\my_packages\\tmpy')
import tmsignals as ts # Custom package
import importlib 
importlib.reload(ts) # Reload custom module on every run

fs, car = wavfile.read("Noisexvolvo_2min.wav")

car_gated = ts.doGate(sig=car,rampdur=0.01,fs=fs)
car_gated = ts.doNormalize(car_gated)

wavfile.write("Noisexvolvo_2min_ramped.wav", fs, car_gated)
