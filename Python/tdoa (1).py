"""
Generalized Cross-correlation - Phase Transform is a Time-difference-of-arrival (TDOA) Algorithm where PHAT is a well-known weighting function
"""
from time import time

# function for measuring run time of functions
def timer_func(func): 
    def wrap_func(*args, **kwargs):
        times = 0
        counter = 100
        for i in range(counter):
            print("running")
            # counter += 1
            # print(counter)
            t1 = time() 
            result = func(*args, **kwargs) 
            t2 = time()
            times += (t2 - t1)
        print(f'Function {func.__name__!r} executed {counter} times, and took on average {times/counter:.4f}s') 
        return result 
    return wrap_func 

# @timer_func
def gcc_phat(sig, refsig, fs=1, max_tau=None, interp=10):
    import numpy as np
    '''
    calculates time delay given a reference signal, refsig, and another signal, sig.
    '''
    n = np.shape(sig)[0] + np.shape(refsig)[0]
    
    window = np.hanning(len(sig)) # applies hanning window before DRFFT (discrete real fast fourier transform)
    
    # applies FFT on both signals and gets the cross power spectral density (CPSD)
    SIG = np.fft.rfft(sig*window, n=n) # rfft has better performance
    REFSIG = np.fft.rfft(refsig*window, n=n)
    G = SIG * np.conj(REFSIG)
    
    # print("G shape", np.shape(G))
    # print("iterp * n", interp*n)
    
    # generalized cross-correlation function multiplied with weighting function, psi.
    psi = 1 / np.abs(G)
    
    # print("gpsi|", np.shape(G * psi))
    
    cc = np.fft.irfft(G * psi, n=(interp * n))
    
    # print("cc", np.shape(cc))
    
    shift = int(interp * n / 2) # where to shift xcorr graph to get negative tau
    # print("cc_len", len(cc))
    # print("shift", shift)
    if max_tau:
        shift = np.minimum(int(interp * fs * max_tau), shift)

    cc = np.concatenate((cc[-shift:], cc[:shift + 1]))
    # print(np.argmax(np.abs(cc)))
    # find max cross correlation index
    argmax = np.argmax(cc) - shift

    tau = argmax / float(interp * fs)
    
    return int(tau), cc

# @timer_func
def find_tau(cc, fs=1, max_tau=None, interp=10):
    shift = int(len(cc) / 2)
    argmax = np.argmax(cc) - shift
    # print("argmax", argmax)
    if abs(argmax) == 1:
        argmax = 0
        
    tau = argmax / float(interp * fs)
    
    return tau

from scipy import signal
import numpy as np
# @timer_func
def gcc_phat_scipy(sig, refsig):
    correlation = signal.correlate(sig, refsig)
    lags = signal.correlation_lags(len(sig), len(refsig))
    lag = lags[np.argmax(correlation)]
    
    return lag, correlation

#testing (run this as main)
def main():
    import numpy as np
    import matplotlib.pyplot as plt
    import tdoa
    from scipy import signal
    
    rng = np.random.default_rng()
    sig = rng.standard_normal(999)
    
    sig1 = np.concatenate((rng.standard_normal(99), sig[:900]))
    sig2 = sig
    sig3 = np.concatenate((rng.standard_normal(99), sig[:900]))
    sig4 = np.concatenate((rng.standard_normal(399), sig[:600]))
    sig5 = np.concatenate((rng.standard_normal(199), sig[:800]))
    
    
    lag12 = tdoa.gcc_phat_scipy(sig2, sig4)
    
    lag12, _ = tdoa.gcc_phat(sig2, sig1)
    print(lag12)
    print(len(_))
    
        
if __name__ == "__main__":
    main()
