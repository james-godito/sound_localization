import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
import pyroomacoustics as pra

def Circle(x, y, r, n):
    points = []
    theta = (np.pi * 2) / n
    
    for i in range(n):
        curr_angle = (theta * i) + np.pi/2
        pointX = (r * np.cos(curr_angle)) + x
        pointY = (r * np.sin(curr_angle)) + y
        points.append((pointX, pointY))
    return points

# =============================================================================
# TO-DO:
# fix ill-conditioned matrix error
# =============================================================================

# Sound source location
azimuth = np.array([45, 135]) / 180 * np.pi # Angular displacement on a spherical (radians) coordinate system from a cardinal direction (+-180)
distance = 4 # meters

# Constants
c = 343 # (m/s) speed of sound
fs = 16000 # sampling frequency based on arduino
nfft = 256 # FFT size
freq_range = [300, 3500]
room_x = 15
room_y = 10
room_z = 5
mics = 5
mic_diameter = 0.06

# Set up the 3d room dimensions
room_dim = [room_x, room_y, room_z]

# Create an anechoic shoebox room
snr_db = 5 # signal to noise ratio
sigma2 = 10 ** (-snr_db / 10) / (4 * np.pi * distance) ** 2

room = pra.ShoeBox(room_dim, fs=fs, max_order=0, sigma2_awgn=sigma2)

circle_points = Circle(room_y/2, room_z/2, mic_diameter, mics)
y_coordinates, z_coordinates = zip(*circle_points)
y_coordinates = list(i for i in y_coordinates)
z_coordinates = list(i for i in z_coordinates)

mic_loc = np.zeros(shape=(mics, 3))

for i in range(mics):
    mic_loc[i] = [0, y_coordinates[i], z_coordinates[i]]
    
mic_loc = mic_loc.T

# the fs of the microphones is the same as the room
mic_array = pra.MicrophoneArray(mic_loc, room.fs)

# finally place the array in the room
room.add_microphone_array(mic_array)

rng = np.random.RandomState(23)
duration_samples = int(fs)

sound_loc = []
for ang in azimuth:
    y_loc = room_y/2 + (distance * np.tan(ang)) # adjusting sound loc to center
    sound_loc.append(y_loc) # for printing
    source_location = np.array([distance, y_loc, room_z*0.5])
    source_signal = rng.randn(duration_samples)
    room.add_source(source_location, signal=source_signal)
    
# Simulate room acoustics
room.simulate()

X = pra.transform.stft.analysis(room.mic_array.signals.T, nfft, nfft // 2)
X = X.transpose([2, 1, 0])

algo_names = ['SRP', 'MUSIC', 'FRIDA', 'TOPS']
spatial_resp = dict()

# loop through algos
for algo_name in algo_names:
    # Construct the new DOA object
    # the max_four parameter is necessary for FRIDA only
    doa = pra.doa.algorithms[algo_name](mic_loc, fs, nfft, c=c, num_src=2, max_four=4)

    # this call here performs localization on the frames in X
    doa.locate_sources(X, freq_range=freq_range)
    
    # store spatial response
    if algo_name == 'FRIDA':
        spatial_resp[algo_name] = np.abs(doa._gen_dirty_img())
    else:
        spatial_resp[algo_name] = doa.grid.values
        
    # normalize   
    min_val = spatial_resp[algo_name].min()
    max_val = spatial_resp[algo_name].max()
    spatial_resp[algo_name] = (spatial_resp[algo_name] - min_val) / (max_val - min_val)
    
# plotting param
base = 1
height = 10
true_col = [0, 0, 0]

# loop through algos
phi_plt = doa.grid.azimuth
for algo_name in algo_names:
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    
    c_phi_plt = np.r_[phi_plt, phi_plt[0]]
    c_dirty_img = np.r_[spatial_resp[algo_name], spatial_resp[algo_name][0]]
    
    ax.plot(c_phi_plt, base + height * c_dirty_img,
            linewidth=3,
            alpha=0.55,
            linestyle='-',
            label="spatial spectrum"
            )
    
    plt.title(algo_name)
    
    # plot true loc
    for angle in azimuth:
        ax.plot([angle, angle], [base, base + height], linewidth=3, linestyle='--',
            color=true_col, alpha=0.6)
    K = len(azimuth)
    ax.scatter(azimuth, base + height*np.ones(K), c=np.tile(true_col,
               (K, 1)), s=500, alpha=0.75, marker='*',
               linewidths=0,
               label='true locations')

    plt.legend()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, framealpha=0.5,
              scatterpoints=1, loc='center right', fontsize=16,
              ncol=1, bbox_to_anchor=(1.6, 0.5),
              handletextpad=.2, columnspacing=1.7, labelspacing=0.1)

    ax.set_xticks(np.linspace(0, 2 * np.pi, num=12, endpoint=False))
    ax.xaxis.set_label_coords(0.5, -0.11)
    ax.set_yticks(np.linspace(0, 1, 2))
    ax.xaxis.grid(color=[0.3, 0.3, 0.3], linestyle=':')
    ax.yaxis.grid(color=[0.3, 0.3, 0.3], linestyle='--')
    ax.set_ylim([0, 1.05 * (base + height)])
    
fig, ax = room.plot()
print("azimuth", azimuth[1] - azimuth[0])
print("mic y, z =", y_coordinates, z_coordinates)
print("sound location =", sound_loc)
plt.show()
