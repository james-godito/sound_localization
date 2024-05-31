# Microphone Array-based Sound Localization

## Introduction

This project presents a novel approach to sound source localization using a Time Difference of Arrival (TDOA) estimation algorithm built on an Arduino platform with a microphone array. The system employs the Generalized Cross-Correlation with Phase Transform (GCC-PHAT) method to accurately determine the direction of a sound source.

## Features

- **GCC-PHAT**: Utilizes the GCC-PHAT algorithm for robust TDOA estimation.
- **Microphone Array**: Leverages a microphone array for capturing sound from different directions.

## Important

This project uses two different Arduino boards, these are the Mega 2560 and uno R4. The reason for this is because the uno has a better sampling rate, but cannot run or support a library needed for the tracking when it comes to the yolo part.
The following files are needed to run the entirety of the project as it was intended.

1. **main_uno.ini

2. **main_mega_servo.ini

3. **main_SSL_and_yolo.py

In addition to all the libraries stated below.
The testing files for each process, the Sound source localization part and Yolo are provided.

## Installation

1. **Download Required Python Modules**: Ensure you have all necessary Python modules. The required libraries are:
   * Pyserial
   * Numpy
   * evenpoints
   * matplotlib
   * tdoa
   * utils
   * Pytorch
   * cv2
   * *VarSpeedServo(arduino lib)

3. **Upload Arduino Codes**: Upload the provided Arduino code to your Arduino IDE compatible boards. Connect your microphones to the AD7606 DAQ module, then connect it and the servos to the board based on the SPI pins on the microcontroller and the user-defined digital pins.

4. **Run the Main Script**: Place the Python modules evenpoints.py, tdoa.py, and utils.py in the same directory as the main script and run main:

## Hardware Requirements

- **Microcontroller Unit (MCU)**: Higher clock speeds yield better performance, but any Arduino can be used if it has enough pins.
- **Microphone Array**: Multiple microphones connected to the AD7606.
- **AD7606 DAQ Module**: Ensure it is configured for the correct communication mode (SPI or Parallel).
- **Servos**: Two servos for pointing towards the sound source.
- **Communication**: The Arduino must support SPI or Parallel communication based on the AD7606 configuration. The AD7606 from Amazon is typically set to Parallel mode by default, which can be changed to Serial by moving the R2 resistor to the R1 position.

## Usage

1. **Connect Hardware**: Assemble the microphone array, connect the AD7606 DAQ module and servos to the Arduino.
2. **Upload Arduino Code**: Open the Arduino IDE, upload the provided code to the board.
3. **Run Python Script**: Execute the main Python script to start the sound localization process.

## References

1. [GCC-PHAT Explanation](https://www.proquest.com/docview/304587883?parentSessionId=rFc8F31XVj3N3lu6u2P9rlxSaNrkf9FaCGTloUOT3mk%3D&sourcetype=Dissertations%20&%20Theses)
2. [AD7606 Datasheet](https://www.analog.com/en/products/ad7606.html)

## Notes
The unused folder in the repository contains an SRP code that has not been properly implemented, but should work theoreticaly with some adjustment.

## License

This project is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.html) file.
