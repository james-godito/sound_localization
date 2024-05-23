# misc. functions
import serial
import struct


# expected start/stop bytes
STX = b'\x02'
ETX = b'\x03'

# data block parameters
offset = 21495
thresh = 2000 # peak threshold
scaleFactor = 5/2**16

# functions
# receive bytes from arduino
def dataRead(arduino, start, end, expected):
    parsed = []
    while len(parsed) < expected / 2:
        curr_byte = arduino.read()
        # print(curr_byte)
        if curr_byte == STX:
            # print("package", arduino.read_until(ETX))
            byte_arr = [byte for byte in arduino.read_until(ETX, expected + 1)]
            # print("BYTE", len(byte_arr))
            # print("byte_arr", byte_arr)
            byte_arr.pop()
            
            for i in range(int(len(byte_arr) / 2)):
                parsed.append((byte_arr[i * 2] << 8)|byte_arr[(i * 2) + 1])
                # print(parsed)
        
        else:
            continue
        
    return [int(i) - offset for i in parsed]

def dataRead_analog(arduino, start, end, expected):
    parsed = []
    while len(parsed) < expected:
        curr_byte = arduino.read()
    # print(curr_byte)
        if curr_byte == STX:
            # print()
            parsed = [byte for byte in arduino.read_until(ETX, 4)]
        #     # print("BYTE", len(byte_arr))
            parsed.pop()
            # print("parsed", parsed)
                
        else:
            continue
        
    return [int(i) for i in parsed]

def data_read(arduino):
    raw_data = arduino.read_until(b'\n')
    dec_data = raw_data.decode().strip()
    data = dec_data.split(',')
    return data

# send to arduino
def dataSend(arduino, data, key="x"):
    if key == "x":
        arduino.write((f"{data}x!").encode())
    
    if key == "y":
        arduino.write((f"{data}y!").encode())

# check if buffer contains peak
def peakDetection(*args, method='all'):
    conds = []
    
    for buffer in args:
        conds.append(abs(max(buffer, key=abs)) >= thresh)
    
    if method == 'all':
        return all(conds)
    
    elif method == 'any':
        return any(conds)

# filter out values below threshold
def ampFilter(vals):
    thresh1 = 1000
    
    for i in range(len(vals)):
        if abs(vals[i]) < thresh1:
            vals[i] = 1
            
    return vals

# verify valid TDE
def verify(ref_delays, delays, sps_error = 3):
    valid = []

    for tau in ref_delays:
        counter2 = 0
        
        for i in range(len(delays[1])):
            for j in range(counter2, len(delays[0]) - 1):
                # can be changed to allow errors of n samples
                # print("i+1, j-counter, j+1, i", i + 1, j - counter2, j + 1, i)
                valid.append(abs((delays[i][j - counter2]) - (tau[j + 1] - tau[i])) < sps_error) 
                
            counter2 += 1
        
        if all(valid) and len(valid) != 0: 
            return tau
        
        else:
            valid.clear()
            
def avg(lst):
    _lst = list(abs(i) for i in lst)
    return sum(_lst) / len(_lst)