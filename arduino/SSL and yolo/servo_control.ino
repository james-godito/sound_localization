#include <VarSpeedServo.h>
#include <SPI.h>
VarSpeedServo servo1; VarSpeedServo servo2;
String inputString = "";         // a string to hold incoming data
unsigned int cont=0;

void setup() 
{
  servo1.attach(9); //lower
  servo2.attach(10); //upper

  Serial.begin(500000);
  Serial.println("Ready");
}
void(* resetFunc) (void) = 0; //declare reset function @ address 0


void loop() 
{

  signed int vel;
  unsigned int pos;
  
  if (Serial.available()) 
  {
    inputString = Serial.readStringUntil('!');
    vel = inputString.toInt();   
    

    if (inputString.endsWith("x"))
    {
      if (vel != 0) 
      {
        servo1.write(vel);
        delay(750);
      }
      else
      {
        servo1.write(vel);
      }
    }

    else if(inputString.endsWith("y"))
    {
      if (vel != 0)
      {
        servo2.write(vel);
        delay(750);
      }
      else
      {
        servo2.write(vel);
      }
    }
  
 
    else if(inputString.endsWith("l"))
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
    else if(inputString.endsWith("u"))
    {if (vel > 2)
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
      pos = servo1.read();
      servo1.write(90, 20, true);        
      pos = servo2.read();
      servo2.write(90 , 20, true);
      int pos;
      delay(2000);
      resetFunc();
    }
    inputString = "";
    

  }
}
