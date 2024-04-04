"""
Generalized Cross-correlation - Phase Transform is a Time-difference-of-arrival (TDOA) Algorithm where PHAT is a well-known weighting function
"""
def gcc_phat(sig, refsig, fs=1, interp=1000):
    import numpy as np
    '''
    calculates time delay given a reference signal, refsig, and another signal, sig.
    '''
    n = np.shape(sig)[0] + np.shape(refsig)[0]
    n = 2 ** int(np.log(n)/np.log(2)) # fft is most efficient when n is a power of 2
    
    # applies FFT on both signals and gets the cross power spectral density (CPSD)
    SIG = np.fft.fft(sig, n=n)
    REFSIG = np.fft.fft(refsig, n=n)
    G = SIG * np.conj(REFSIG)
    
    # print("G shape", np.shape(G))
    # print("iterp * n", interp*n)
    
    # generalized cross-correlation function multiplied with weighting function, psi.
    psi = 1 / np.abs(G)
    
    # print("gpsi|", np.shape(G * psi))
    
    cc = np.fft.ifft(G * psi, n=(interp * n))
    
    # print("cc", np.shape(cc))
    
    shift = int(interp * n / 2) # where to shift xcorr graph to get negative tau
    
    cc = np.concatenate((cc[-shift:], cc[:shift + 1]))

    # find max cross correlation index
    argmax = np.argmax(np.abs(cc)) - shift

    tau = argmax / float(interp * fs)
    
    return tau, cc

#testing (run this as main)
def main():
    import numpy as np
    import matplotlib.pyplot as plt
    
    refsig = np.linspace(1, 10, 10)
    
    for i in range(0, 10):
        sig = np.concatenate((np.linspace(0, 0, i), refsig, np.linspace(0, 0, 10 - i)))
        ref = np.concatenate((np.linspace(0, 0, 10 - i), refsig, np.linspace(0, 0, i)))
        # ref = np.array([0, 0, 0, 0, 1, 2, 3, 4])
        print("signal: ", sig)
        print("\n")
        print("ref. signal: ", ref)
        offset, _ = gcc_phat(sig, ref)
        print("offset", offset)
        print("-----------------------------------")
    
    print("\n")
    print(np.shape(ref))
    print(np.shape(sig))
    print(np.shape(_))
    plt.plot(_)
        
if __name__ == "__main__":
    main()