#include <Servo.h>

int i = 0;
int centerX = 0; // Initialize centerX to 0
int centerY = 0; // Initialize centerY to 0
String centerPxStr; // Store the received string

// Center box of image feed - if inside this box, no move
int x_min = 900;
int x_max = 1020;

Servo myServo;

void setup() {
    myServo.attach(3);
    Serial.begin(9600); // Initialize serial communication
    myServo.write(90);
}

// ... (previous code remains unchanged)

void loop() {
    // Check if data is available on the serial port
    if (Serial.available() > 0) {
        // Read the incoming value from Python as a string
        centerPxStr = Serial.readStringUntil(')'); // Read until closing parenthesis

        // Parse the string to extract centerX and centerY
        int commaPos = centerPxStr.indexOf(',');
        if (commaPos != -1) {
            centerX = centerPxStr.substring(0, commaPos).toInt(); // Extract centerX
            //centerY = centerPxStr.substring(commaPos + 1).toInt(); // Extract centerY
        }


        
        int targetAngle = map(centerX, x_min, x_max, 0, 180);

        // Smoothly adjust servo position
        int currentAngle = myServo.read();
        while (currentAngle != targetAngle) {
            if (currentAngle < targetAngle) {
                currentAngle += 1;
            } else {
                currentAngle -= 1;
            }
            myServo.write(currentAngle);
            delay(10); // Add a small delay for smooth motion
        }


    }
}
