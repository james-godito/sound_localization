# Note: calculations assume far field conditions

import numpy as np
from scipy.fft import rfft
import evenpoints
import matplotlib.pyplot as plt


nfft = 999 # adjust accordingly
c = 343
fs = 2000
max_bin = int(nfft / 2) + 1
non_zero = 1e-14 # for replacing zeros in matrix


def polar2cart(theta, phi, r=1): # polar coord. to cartesian
    '''
    Parameters
    ----------
    theta, phi : radians
        horizontal angle, from x-axis and elevation angle, from xy-plane, respectively
    r : int
        radius of sphere
        
    Returns
    -------
    np.array([dx, dy, dz]) : ndarray
        direction vector
    '''
    
    phi = phi * np.pi / 180
    theta = phi * np.pi / 180    
    
    dx = r * np.cos(phi) * np.cos(theta)
    dy = r * np.cos(phi) * np.sin(theta)
    dz = r * np.sin(phi)
    
    return np.array([dx, dy, dz])


def cart2polar(x, y, z): # cartesian coord. to polar
    '''
    Parameters
    ----------
    x, y, z : int
        amount of sources to look for, default = 1
        
    Returns
    -------
    theta, phi : degrees
        horizontal angle, azimuth, and vertical angle, elevation        
    '''
    
    phi = np.arcsin(z)
    theta = np.arcsin(y / np.cos(phi))
    
    phi = phi / np.pi * 180
    theta = theta / np.pi * 180
    
    return theta, phi


def loc_grid(azi_range, ele_range): # creates array of candidate locations to evaluate
    '''
    Parameters
    ----------
    azi_range, ele_range : ndarray
        array to iterate thru for azimuth and elevation, respectively
        
    Returns
    -------
    grid : ndarray
        grid points to evaluate; has shape 3 x (len(azi_range) * len(ele_range))
    '''

    grid = np.zeros((3, len(azi_range) * len(ele_range))) # 3 for 3 dimensions
    # print('grid.shape', np.shape(grid))
    
    for i in range(len(azi_range)):
        for j in range(len(ele_range)):
            grid[:, i * len(ele_range) + j] = polar2cart(azi_range[i], ele_range[j])
            # print('index', i*len(ele_range) + j)
    
    return grid

            
def steering_delays(grid, mic_locs): # converts grid array to steering delay array of same shape
    '''
    Parameters
    ----------
    grid : ndarray
        grid points to evaluate; has shape 3 x (len(azi_range) * len(ele_range))
    mic_locs : ndarray
        cartesian coordinates of microphones in mic arrays local coordinate system; has shape 3 x M, where M is mic amount
        
    Returns
    -------
    delta : ndarray
        array of steering delays based on grid of candidate search points
        
    '''

    mics = np.shape(mic_locs)[1]
    locs = np.shape(grid)[1]
    delta = np.zeros((max_bin, mics, locs), dtype=np.complex_)
    
    freq_bins = 1j * 2 * np.pi * np.linspace(0, nfft/2, max_bin) * 1.0 / nfft
    
    for i in range(locs):
        loc = grid[:, i]
        for m in range(mics):
            mic_loc = mic_locs[:, m]
            tau = fs * np.dot(loc, mic_loc) / c
            
            delta[:, m, i] = np.exp(freq_bins * tau)
    
    return delta


def srp(cc_list, delta, grid):
    '''
    Parameters
    ----------
    grid : ndarray
        grid points to evaluate; has shape 3 x (len(azi_range) * len(ele_range))
    mic_locs : ndarray
        cartesian coordinates of microphones in mic arrays local coordinate system; has shape 3 x M, where M is mic amount
        
    Returns
    -------
    src : ndarray
        cartesian coord. of sound source
    azimuth, elevation : degrees
        azimuth and elevation in degrees
    '''
    
    locs = np.shape(delta)[2]
    mics = np.shape(cc_list)[0]
    pairs = mics * (mics - 1) / 2
    P = np.zeros(locs)
    # print('P:', np.shape(P))
    
    x = cc_list
    absx = abs(cc_list)
    absx[absx < non_zero] = non_zero    
    pX = x/absx # PHAT weighting
    
    for i in range(locs):
        Yk = pX.T * delta[:,:,i]
        CC = np.dot(Yk, np.conj(Yk).T) # GCC-PHAT
        P[i] = P[i] + abs(np.sum(np.triu(CC, 1))) / max_bin / pairs # SRP, Note: np.triu makes calculations faster
    
    peak_n = 4 # number of peaks to average
    peaks = P.argsort()[-peak_n::][::-1] # returns index of peaks, Note: sorts in descending order
    results = grid[:, peaks]
    src = np.average(results, axis=1) # cartesian coords
    
    # print("results", results)
    # plt.plot(P)
    # idx = np.argmax(P)
    # src = grid[:,idx]
    
    azimuth, elevation = cart2polar(src[0], src[1], src[2])
    
    return src, azimuth, elevation
        

def main(): # for testing
    locs = evenpoints.circle(0, 0, .2744/2, 5)
    
    mic_loc = np.zeros((3, 5))
    
    for i in range(len(locs)):
        mic_loc[1, i] = locs[i][0]
        mic_loc[2, i] = locs[i][1]
    
    
    # sig = np.concatenate((np.linspace(0, 0, 101), np.linspace(0, 800, 2), np.linspace(4, 1, 2), np.linspace(0, 0, 291)))
    # print(mic_loc)
    
    rng = np.random.default_rng()
    sig = rng.standard_normal(999)
    window = np.hanning(len(sig))
    # sig1 = np.concatenate((rng.standard_normal(99), sig[:900]))
    # sig2 = sig
    # sig3 = np.concatenate((rng.standard_normal(99), sig[:900]))
    # sig4 = np.concatenate((rng.standard_normal(399), sig[:600]))
    # sig5 = np.concatenate((rng.standard_normal(199), sig[:800]))
    
    sig1 = sig * window
    sig2 = sig * window
    sig3 = sig * window
    sig4 = sig * window
    sig5 = sig * window
    # print(np.shape(rfft(sig1)))
    
    cc_list = np.zeros((5 , len(rfft(sig1))), dtype=np.complex128)
    cc_list[0,] = rfft(sig1)
    cc_list[1,] = rfft(sig2)
    cc_list[2,] = rfft(sig3)
    cc_list[3,] = rfft(sig4)
    cc_list[4,] = rfft(sig5)
    
    resolution = 11
    azi_range = np.linspace(80, -80, resolution)
    ele_range = np.linspace(45, -45, resolution)
    
    # print(azi_range)
    # print(ele_range)
    grid = loc_grid(azi_range, ele_range) # spherical grid of candidate directions
    delta = steering_delays(grid, mic_loc) # steering delay for each mic based on grid

    # print(grid)
    # print('delta', np.shape(delta))
    print(srp(cc_list, delta, grid))

if __name__ == '__main__':
    main()