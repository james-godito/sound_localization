#include <Servo.h>

int centerX = 0; // Initialize centerX to 0
String centerPxStr; // Store the received string

// Center box of image feed - if inside this box, no move
int x_min = 800;
int x_max = 1120;
int deg=90;

Servo myServo;

void setup() {
    myServo.attach(3);
    Serial.begin(9600); // Initialize serial communication
    myServo.writeMicroseconds(1500); // Set the initial position to stop the servo
}

void loop() {
    // Check if data is available on the serial port
    if (Serial.available() > 0) {
        // Read the incoming value from Python as a string
        centerPxStr = Serial.readStringUntil(')'); // Read until closing parenthesis

        // Parse the string to extract centerX
        int commaPos = centerPxStr.indexOf(',');
        if (commaPos != -1) {
            centerX = centerPxStr.substring(0, commaPos).toInt(); // Extract centerX
        }
        
        if(centerX<x_min || centerX>x_max){
            if (centerX < x_min) {
                deg+=5;
                myServo.write(deg); // Set the servo to rotate in one direction
            } 
            else if (centerX > x_max) {
                deg-=5;
                myServo.write(deg); // Set the servo to rotate in the other direction
            }
            else{
              deg=deg;
            }

            delay(10);
        }
        else{
          myServo.write(deg);
        }
    }
}
