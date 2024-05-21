import serial
import numpy as np
import evenpoints
import matplotlib.pyplot as plt
import tdoa
from utils import *

# ---------------------
# AD7606 Pins
# ---------------------

# Arduino MEGA 2560 R3
# ---------------------
# BUSY 32               // you can use any digital pin   
# RESET 30              // you can use any digital pin  
# START_CONVERSION 34   // you can use any digital pin    
# CHIP_SELECT 53        // SPI CS     
# D7_out 50             // SPI MISO there is no need to use MOSI port with the ad7606 
# RD 52                 // SPI SCLK 
# RANGE 36              // you can use any digital pin 

# Arduino UNO R4 Wifi
# ---------------------
# BUSY 8                // you can use any digital pin   
# RESET 9               // you can use any digital pin  
# START_CONVERSION 7    // you can use any digital pin    
# CHIP_SELECT 10        // SPI CS     
# D7_out 12             // SPI MISO there is no need to use MOSI port with the ad7606 
# RD 13                 // SPI SCLK 
# RANGE 36              // you can use any digital pin

# Servos
# ---------------------
# Arduino UNO R4 Wifi
# Lower servo 5
# Upper servo 6

# Note:
# -------------------------------------------------------------
# elevation = 180, moves upper servo down
# azimuth = 180, moves upper servo right (facing array)
# -------------------------------------------------------------

# buffers for data block and advance blocks
buffers = [[], [], []]
delays = [[], [], []]
adv = [[], [], []]

# serial communication variables
port1 = 'COM7'
port2 = 'COM3'
baudrate = 500000


# data read settings
byteOrder = 'big'
bytes2Read = 6 # 16 bit res and 8 channels leading to 16 bytes, 5 channels = 10 byes


# initialize serial communication
arduino_uno = serial.Serial(port1, baudrate)
# arduino_mega = serial.Serial(port2, baudrate)


c = 343 # sound speed


# data block parameters
interp = 10
scaler = 2.5/(2**16)
# fs = 6080 # sampling rate simple on uno, analog read only
fs = 2120 # 3 mics and data sending function: ~467 us conversion time.
# fs = 760 # arduino mega 2560 sampling rate
block_n = 40 # number of blocks per second
block = fs // block_n
advance = int(block * .5)
overlap = int(block * .5)


# mic array parameters
mics = 3
mic_radius = 0.2744
mic_dist = 0.26097 # largest pair distance
max_delay = mic_dist / c # 0.000760932944606414 s
max_ele_delay = 5.601299294e-09

# data block processing params
Peaks = 3 # empirically decided
thresh = 6
azi_range = (30, 150) # lower servo move range
ele_range = (45, 135) # upper servo move range


# initialize mic locations
locs = evenpoints.circle(0, 0, mic_radius/2, mics)
mic_loc = np.zeros((3, mics))

for i in range(mics):
    mic_loc[1, i] = locs[i][0]
    mic_loc[2, i] = locs[i][1]

counter1 = 0
lag_amount = 5 # number of lags to average

print("Starting...")
while True:
    vals = dataRead(arduino_uno, STX, ETX, bytes2Read)
    
    if (len(buffers[-1]) < block): # checks if buffer is full, and fills it if not
        for i in range(mics):
            buffers[i].append(vals[i])
            
            
    if (len(buffers[-1]) == block):
        if (len(adv[-1]) == advance): # once buffers and advance buffers are full start localization algorithm  
            _12, cc12 = tdoa.gcc_phat(buffers[0], buffers[1]) # pair-wise correlations using gcc-phat
            _13, cc13 = tdoa.gcc_phat(buffers[0], buffers[2])
            _23, cc23 = tdoa.gcc_phat(buffers[1], buffers[2])
            
            if _23 == 2: # during testing the sample lags sometimes become 2, so to avoid suddenly moving the camera, set it to 0
                _23 = 0
                
            if _23 != 0: # checks if the delays are 0 or not
                delays[0].append(_23) # if not zero append to the delays buffer
                counter1 = 0 # and reset the counter to 0
            
            elif _12 != 0:
                delays[1].append(_12)
                counter1 = 0
            
            elif _13 != 0:
                delays[2].append(_13)
                counter1 = 0
            
            else: # if delay is zero, increment counter by 1
                counter1 += 1
                
            if (counter1 == lag_amount) and (len(delays[0]) != 0): # if the amount of zeros between non zeroes is equal to a given amount AND the delay buffer is not empty, calculate position to send to servos.
                counter1 = 0 # reset counter
                
                lag_azi = np.sum(delays[0]) / len(delays[0]) # take the average of mic pair 23, corresponds to the lag used to find the azimuth
                lag_ele = (np.sum(delays[1]) + np.sum(delays[2]))
                lag_ele = lag_ele / 2 # take the average of mic pairs 13 and 12, corresponds to the lag used to find the elevation
                
                delays[0].clear() # clear the delay buffers
                delays[1].clear()
                delays[2].clear()
                
                if (np.isnan(lag_azi) != True) and (np.isnan(lag_ele) != True):
                # lag_azi and lag_ele are nans (not a number) when 
                    
                    if lag_azi == 2: # during testing the sample lags sometimes become 2, so to avoid suddenly moving the camera, set it to 0
                        lag_azi -= 2
                    
                    print("lag_azi", lag_azi) # for debugging
                    print("lag_ele", lag_ele)
                    
                    lag_azi = lag_azi / fs # divide the sample lags with the sampling frequency to find the time equivalent
                    lag_ele = lag_ele / fs
                    
                    if abs(lag_azi) > max_delay: # additional check to see if the delay is greater than expected, and sets it to max delay if True.
                        if lag_azi < 0:
                            lag_azi = - max_delay
                        else:
                            lag_azi = max_delay
                            
                    if abs(lag_ele) > max_delay:
                        if lag_ele < 0:
                            lag_ele = - max_delay
                        else:
                            lag_ele = max_delay
                    
                    azimuth = 180 - ((np.arccos((lag_azi * c) / mic_dist) / np.pi) * 180) # "180 -" part is to set the default angle to 90, which rotates the servo to point to the front. The np.pi and 180 is to convert radian to degrees
                    elevation = 180 - ((np.arccos((lag_ele * c) / mic_dist) / np.pi) * 180)
                    
                    if azimuth > azi_range[1]: # limit the movement range of the servos on pc side instead of arduino to increase sampling rate a little.
                        dataSend(arduino_uno, azi_range[1])
                            
                    elif azimuth < azi_range[0]:
                        dataSend(arduino_uno, azi_range[0])
                      
                    else:
                        dataSend(arduino_uno, int(azimuth))
                        
                    if elevation > ele_range[1]:
                        dataSend(arduino_uno, ele_range[1], key='y')
                            
                    elif elevation < ele_range[0]:
                        dataSend(arduino_uno, ele_range[0], key='y')
                      
                    else:
                        dataSend(arduino_uno, elevation, key="y")
            
            elif (counter1 == lag_amount): # if the number of zero delays between non zeros is equal to a given amount and the delay buffer is empty, reset the camera to default position
                dataSend(arduino_uno, 90)
                dataSend(arduino_uno, 90, key="y")
            
            # print("Advancing block...")
            for i in range(mics): # advances block according to parameters defined
                buffers[i] = buffers[i][-overlap:] + adv[i]
                adv[i].clear()   
            
        for i in range(mics): # after buffer is full, only the advance buffer is filled
            adv[i].append(vals[i])

