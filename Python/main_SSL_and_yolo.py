import serial
from threading import Timer
import numpy as np
from scipy import signal
import evenpoints
import matplotlib.pyplot as plt
import tdoa
from utilz import *
import torch
import cv2
from time import sleep
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
cap = cv2.VideoCapture(2)
frame_w = 1280
frame_h = 720
set_res(cap, frame_w, frame_h)
port1 = 'COM7'
port2 = 'COM3'
baudrate = 500000
arduino_uno = serial.Serial(port1, baudrate)
arduino_mega = serial.Serial(port2, baudrate)



# Load YOLOv5 model (change the path to your trained model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
def yolo(bool_yolo):
    # Capture frame-by-frame
    while bool_yolo==True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
    
        # Our operations on the frame come here
        # Perform inference using YOLOv5
        results = model(frame)
    
        # Get coordinates of detected people
        detections = results.xyxy[0].cpu().numpy()
    
        # Filter detections to include only people (class 0)
        people_detections = detections[detections[:, -1] == 0]
    
        # Draw bounding boxes for people
        for det in people_detections:
            x, y, w, h, conf, cls = det
            x, y, w, h = int(x), int(y), int(w), int(h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
        # Display the resulting frame
        cv2.imshow('frame', frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            bool_yolo=False
            
        
        
        
        
            
        if people_detections.shape[0] > 0:
            # Assuming the first detected person is the closest one
            face_center_x = people_detections[0, 0] + people_detections[0, 2] / 2
            face_center_y = people_detections[0, 1] + people_detections[0, 3] / 2
    
            err_x = 30 * (face_center_x - frame_w / 2) / (frame_w / 2)
            err_y = 30 * (face_center_y - frame_h / 2) / (frame_h / 2)
    
            arduino_mega.write((f"{err_x}l!").encode())
            if err_y>=100:
                err_y=100
            arduino_mega.write((f"{err_y}u!").encode())
            # print(err_y,err_x)
            # print("YOLO")
        else:
        
            arduino_mega.write("o!".encode())
            startMain=Timer(10, main())
            startMain.start()
            startMain.join()
            break
            bool_yolo=False
            print("break")
            
            
           

    

def main():
    buffers = [[], [], []]
    delays = [[], [], []]
    adv = [[], [], []]
    cc = [[], [], []] # cross-correlation list [[12, 13, 14, 15], [23, 24, 25], [34, 35], [45]]
    ref_delays = [[], [], [], []] # reference delays for 1i pairs (e.g. 12, 13, 14, 15)
    ref_delays2 = [[], [], []]

    # serial communication variables
   

    # data read settings
    byteOrder = 'big'
    bytes2Read = 6 # 16 bit res and 8 channels leading to 16 bytes, 5 channels = 10 byes


    # initialize serial communication
   


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
    ele_range = (45, 100) # upper servo     "

    lags = signal.correlation_lags(block, block) # initialize lags for scipy method


    window = np.hanning(block) # hanning window function

    # initialize mic locations
    locs = evenpoints.circle(0, 0, mic_radius/2, mics)
    mic_loc = np.zeros((3, mics))

    

    

    for i in range(mics):
        mic_loc[1, i] = locs[i][0]
        mic_loc[2, i] = locs[i][1]


    test_lags = []
    test_lags_ele = []
    counter = 0
    counter1 = 0
    counter2 = 0
    lag_amount = 5

    t1_start=0
    t1_stop=0



    bool_yolo= False     
    print("Starting...")
    while True:
        
        vals = dataRead(arduino_uno, STX, ETX, bytes2Read)
        # vals = arduino_uno.read(5)
        # print("avg vals", avg(vals))
        #print(vals)
        if (len(buffers[-1]) < block):
            for i in range(mics):
                buffers[i].append(vals[i])
                
        
        if (len(buffers[-1]) == block):
            # print("Block full.")
            if (len(adv[-1]) == advance):
                # print("adv full")
                if (bool_yolo==False):
                # correlation25 = signal.correlate(buffers[0], buffers[2], mode='full')
                # correlation12 = signal.correlate(buffers[0], buffers[1], mode='full')
                # correlation15 = signal.correlate(buffers[0], buffers[2], mode='full')
                
                # correlation34 = signal.correlate(buffers[2], buffers[3], mode='full')
                # correlation13 = signal.correlate(buffers[0], buffers[2], mode='full')
                # correlation14 = signal.correlate(buffers[0], buffers[3], mode='full')
                
                # index25 = np.argmax(correlation25)
                # index12 = np.argmax(correlation12)
                # index15 = np.argmax(correlation15)
                
                # correlation25[index25] = 0
                # correlation13[index13] = 0
                # correlation14[index14] = 0
                
                    _12, cc12 = tdoa.gcc_phat(buffers[0], buffers[1])
                    _15, cc15 = tdoa.gcc_phat(buffers[0], buffers[2])
                    _25, cc25 = tdoa.gcc_phat(buffers[1], buffers[2])
                    
                    if _25 == 2:
                        _25 = 0
                    print("mic25", _25)
                    # print("mic15", _15)
                    if _25 != 0:
                        delays[0].append(_25)
                        counter1 = 0
                    
                    elif _12 != 0:
                        delays[1].append(_12)
                        counter1 = 0
                    
                    elif _15 != 0:
                        delays[2].append(_15)
                        counter1 = 0
                    
                    else:
                        counter1 += 1
                        
                    if (counter1 == lag_amount) and (len(delays[0]) != 0):
                        counter1 = 0
                        lag_azi = np.sum(delays[0]) / len(delays[0])
                        lag_ele = (np.sum(delays[1]) + np.sum(delays[2]))
                        lag_ele = lag_ele / 2
                        
                        delays[0].clear()
                        delays[1].clear()
                        delays[2].clear()
                        
                        if (np.isnan(lag_azi) != True) and (np.isnan(lag_ele) != True):
                            
                            
                            if lag_azi == 2:
                                lag_azi -= 2
                            
                            #print("lag_azi", lag_azi)
                                
                            #print("lag_ele", lag_ele)
                            lag_azi = lag_azi / fs
                            lag_ele = lag_ele / fs
                            
                            if abs(lag_azi) > max_delay:
                                if lag_azi < 0:
                                    lag_azi = - max_delay
                                else:
                                    lag_azi = max_delay
                                    
                            if abs(lag_ele) > max_delay:
                                if lag_ele < 0:
                                    lag_ele = - max_delay
                                else:
                                    lag_ele = max_delay
                            
                            azimuth = 180 - ((np.arccos((lag_azi * c) / mic_dist) / np.pi) * 180)
                            elevation = 180 - ((np.arccos((lag_ele * c) / mic_dist) / np.pi) * 180)
                            # print("azimuth:   ",azimuth, "elevation:    ",elevation)
                            
                            if azimuth > azi_range[1]:
                                dataSend(arduino_mega, azi_range[1])
                                    
                                print(azimuth)
                            elif azimuth < azi_range[0]:
                                dataSend(arduino_mega, azi_range[0])
                              
                            else:
                                dataSend(arduino_mega, int(azimuth))
                                
                            if elevation > ele_range[1]:
                                dataSend(arduino_mega, ele_range[1], key='y')
                                
                                    
                            elif elevation < ele_range[0]:
                                dataSend(arduino_mega, ele_range[0], key='y')
                                
                              
                            else:
                                dataSend(arduino_mega, elevation, key="y")
                            
                            
                            bool_yolo= True
                        if (bool_yolo==True):    
                            yolo(bool_yolo)
                            continue
                                
                               
                                    
                                
                                
                        
                elif (counter1 == lag_amount):
                    dataSend(arduino_mega, 90)
                    dataSend(arduino_mega, 90, key="y")
                        
               
                
                 
                for i in range(mics):
                    buffers[i] = buffers[i][-overlap:] + adv[i]
                    adv[i].clear()   
                
            for i in range(mics):    
                adv[i].append(vals[i])

main()
arduino_mega.close()
cap.release()
cv2.destroyAllWindows()


