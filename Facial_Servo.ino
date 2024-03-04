#include <VarSpeedServo.h>
VarSpeedServo servo1; VarSpeedServo servo2;
String inputString = "";         // a string to hold incoming data
unsigned int cont=0;

void setup() 
{
  servo1.attach(9);
  servo2.attach(10);

  Serial.begin(250000);
  Serial.println("Ready");
}


void loop() 
{

  signed int vel;
  unsigned int pos;
  
  if (Serial.available()) 
  {
    inputString = Serial.readStringUntil('!');
    vel = inputString.toInt();   

    if(inputString.endsWith("x"))
    {
      if (vel > 2)
        servo1.write(180, vel, false);    
      else if (vel < -2)
        servo1.write(0, -vel, false);    
      else
      {
        pos = servo1.read();
        servo1.write(pos, 255, false);       
      } 
    }
    else if(inputString.endsWith("y"))
    {
      if (vel > 2)
        servo2.write(180, vel, false);    
      else if (vel < -2)
        servo2.write(0, -vel, false);    
      else
      {
        pos = servo2.read();
        servo2.write(pos, 255, false);       
      } 
    }
    else if(inputString.endsWith("o"))
    {
      cont++;
      if (cont >= 100)
      {
        pos = servo1.read();
        servo1.write(90, 20, true);        
        pos = servo2.read();
        servo2.write(70 , 20, true);
        cont = 0;
 
      }
      else
      {
        pos = servo1.read();
        servo1.write(pos, 255, false);        
        pos = servo2.read();
        servo2.write(pos, 255, false);
      }
      
            
    }
    inputString = "";

  }
}
