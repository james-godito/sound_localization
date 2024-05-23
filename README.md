# Microphone Array-based Sound Localization

## Introduction

This project presents a novel approach to sound source localization using a Time Difference of Arrival (TDOA) estimation algorithm built on an Arduino platform with a microphone array. The system employs the Generalized Cross-Correlation with Phase Transform (GCC-PHAT) method to accurately determine the direction of a sound source.

## Features

- **GCC-PHAT**: Utilizes the GCC-PHAT algorithm for robust TDOA estimation.
- **Microphone Array**: Leverages a microphone array for capturing sound from different directions.

## Installation

1. **Download Required Python Modules**: Ensure you have all necessary Python modules. You can install them using pip:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: Create a `requirements.txt` file listing all needed Python packages if not already provided.)

2. **Upload Arduino Code**: Upload the provided Arduino code to your Arduino IDE compatible board. Connect your microphones, AD7606 DAQ module, and servos to the board as per the hardware requirements.

3. **Run the Main Script**: Place the Python modules in the same directory as the main script and run it:
   ```bash
   python main.py
   ```

## Hardware Requirements

- **Microcontroller Unit (MCU)**: Higher clock speeds yield better performance, but any Arduino can be used if it has enough pins.
- **Microphone Array**: Multiple microphones connected to the Arduino.
- **AD7606 DAQ Module**: Ensure it is configured for the correct communication mode (SPI or Parallel).
- **Servos**: Two servos for pointing towards the sound source.
- **Communication**: The Arduino must support SPI or Parallel communication based on the AD7606 configuration. The AD7606 from Amazon is typically set to Parallel mode by default, which can be changed to Serial by moving the R2 resistor to the R1 position.

## Usage

1. **Connect Hardware**: Assemble the microphone array, connect the AD7606 DAQ module and servos to the Arduino.
2. **Upload Arduino Code**: Open the Arduino IDE, upload the provided code to the board.
3. **Run Python Script**: Execute the main Python script to start the sound localization process.

## References

1. [GCC-PHAT Explanation](https://www.proquest.com/docview/304587883?parentSessionId=rFc8F31XVj3N3lu6u2P9rlxSaNrkf9FaCGTloUOT3mk%3D&sourcetype=Dissertations%20&%20Theses)
2. [AD7606 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ad7606.pdf)

## License

This project is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](LICENSE) file.
