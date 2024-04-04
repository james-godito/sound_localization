import tdoa
from triangulation import triangulation
import serial
import numpy as np
import evenpoints as ep
import matplotlib.pyplot as plt

def data_read(): # reads and processes data from arduino
    raw_data = arduino.read_until(b'\n')
    dec_data = raw_data.decode().strip()
    data = dec_data.split(',')
    return data

port = 'COM3'
baudrate = 115200
arduino = serial.Serial(port, baudrate, timeout=.1)

fs = 550 # sampling frequency [Hz] take from written arduino code (assuming 5 mics)
sample_len = 2 # sec
mics = 5 # number of mics
mic_diameter = 0.2744 # [m]
buffer_n = int(np.log(fs)/np.log(2))
buffer_size = 2**(buffer_n)

mic1_buffer = [] # buffer for each mic
mic2_buffer = []
mic3_buffer = []
mic4_buffer = []
mic5_buffer = []
tau_buffer = np.zeros((mics, 1))
mic_pos = np.zeros((mics, 3))

coords = ep.circle(0, 0, mic_diameter/2, mics)

plt.ion() #enable interactive mode
fig = plt.figure()
ax = fig.add_subplot(111) #1x1 plot, subplot 1
plt.ylim([0, 5])
plt.xlim([])

for i in range(np.shape(coords)[0]):
    for j in range(2):
        mic_pos[i, j] = coords[i, j]

while True:
    vals = data_read()
    # print(vals)
    
    if (len(vals) == mics) and (len(mic1_buffer) < fs): # appends sensor data to buffer if buffer is lesser than sampling frequency
        mic1_buffer.append(float(vals[0]))
        mic2_buffer.append(float(vals[1]))
        mic3_buffer.append(float(vals[2]))
        mic4_buffer.append(float(vals[3]))
        mic5_buffer.append(float(vals[4]))
        
    # print(mic1_buffer)
    # print(mic2_buffer)
    
    elif (len(vals) == mics) and (len(mic1_buffer) == fs): # applies gcc phat
        tau1, _ = tdoa.gcc_phat(mic1_buffer, mic2_buffer, fs=fs)
        tau2, _ = tdoa.gcc_phat(mic2_buffer, mic3_buffer, fs=fs)
        tau3, _ = tdoa.gcc_phat(mic3_buffer, mic4_buffer, fs=fs)
        tau4, _ = tdoa.gcc_phat(mic4_buffer, mic5_buffer, fs=fs)
        tau5, _ = tdoa.gcc_phat(mic5_buffer, mic1_buffer, fs=fs)
        
        tau_buffer[0, 0] = tau1
        tau_buffer[1, 0] = tau2
        tau_buffer[2, 0] = tau3
        tau_buffer[3, 0] = tau4
        tau_buffer[4, 0] = tau5
        
        print(f"Tau 1 = {tau1}")
        print(f"Tau 2 = {tau2}")
        print(f"Tau 3 = {tau3}")
        print(f"Tau 4 = {tau4}")
        print(f"Tau 5 = {tau5}")
        
        mic1_buffer.pop(0) # "moves" window one sample forward. (removes 1st sample and adds newest)
        mic1_buffer.append(float(vals[0]))
        mic2_buffer.pop(0)
        mic2_buffer.append(float(vals[1]))
        mic3_buffer.pop(0)
        mic3_buffer.append(float(vals[2]))
        mic4_buffer.pop(0)
        mic4_buffer.append(float(vals[3]))
        mic5_buffer.pop(0)
        mic5_buffer.append(float(vals[4]))
        
        print(triangulation(mic_pos, tau_buffer))
        
        