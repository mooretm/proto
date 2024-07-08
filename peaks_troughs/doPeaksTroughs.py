import numpy as np
import matplotlib.pyplot as plt

from tmpy import tmsignals as ts
import importlib
importlib.reload(ts)

def doPeaksTroughs(sig):
    peaks = np.array([0])
    troughs = np.array([0])
    ind_p = np.array([0])
    ind_t = np.array([0])

    RANGE = 5;   # look within this many slots before and after selected slot

    x1 = sig[1:] - sig[0:len(sig)-1]  # first derivative
    x2 = x1[1:] - x1[0:len(x1)-1] # second derivative

    # find where 1st derivative is (near) zero
    xprod = x1[1:] * x1[0:len(x1)-1]

    """
    # Not sure about this for loop...
    kz = np.where(xprod==0)  # find exact 0s
    for ik in np.arange(1,len(kz),2): # is this right??
        indx_next = kz(ik+1)
        if xprod(indx_next):
            print('Fatal Error in doPeaksTroughs'); # should be 0 too
            return
        print('Warning, Exact 0 found in 1st derivative\n')
        xprod[indx_next] = 1; # set to positive value
    """

    # now pick out 0s and negatives
    zr1 = np.where(xprod<=0)
    zr1 = zr1[0] # np.where returns a tuple - need the array

    pk_tr = x2[zr1] # peaks flagged with negative 2nd deriv; troughs with positive

    # fill in return values
    for kk in np.arange(0,len(zr1)): # DOES THIS NEED +1? 
        if pk_tr[kk]>0:      # a trough
            min_indx = np.max(zr1[kk]-RANGE)
            # If RANGE tries looking at values before 0, set min to 1
            # (negative indeces don't exit and cause a cryptic error)
            if min_indx < 0:
                min_indx = 1
            max_indx = np.min(zr1[kk]+RANGE)
            #[troughs[count_tr], ind] = np.min(sig[min_indx:max_indx])
            troughs = np.append(troughs, np.min(sig[min_indx:max_indx]))
            #ind_t[count_tr] = min_indx + ind - 1
            ind_t = np.append(ind_t, np.mean([min_indx,max_indx])+1)
        else:
            min_indx = np.max(zr1[kk]-RANGE)
            # If RANGE tries looking at values before 0, set min to 1
            # (negative indeces don't exit and cause a cryptic error)
            if min_indx < 0:
                min_indx = 1
            max_indx = np.min(zr1[kk]+RANGE)
            #[peaks[count_pk], ind] = np.max(sig[min_indx:max_indx])
            peaks = np.append(peaks, np.max(sig[min_indx:max_indx]))
            #ind_p[count_pk] = min_indx + ind - 1
            ind_p = np.append(ind_p, np.mean([min_indx,max_indx])+1)

    return peaks, ind_p, troughs, ind_t

#t,sig = ts.mkTone(100,0.2)
sig = ts.mkNoise(np.arange(10,1000),0.05,48000)
sig = ts.doGate(sig,0.01)
peaks, ind_p, troughs, ind_t = doPeaksTroughs(sig)
plt.plot(sig)
plt.plot(ind_p,peaks,'x')
plt.plot(ind_t,troughs,'o')
plt.title('Find peaks and troughs')
plt.show()
