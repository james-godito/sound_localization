#include <VarSpeedServo.h>
VarSpeedServo servo1; VarSpeedServo servo2;
String input = "";         
unsigned int cont=0;

void setup() 
{
  servo1.attach(9);        //servo pins
  servo2.attach(10);

  Serial.begin(500000);    //baudrate of project is 500000
  Serial.println("Ready");
}


void loop() 
{

  signed int velocity;
  unsigned int position;
  
  if (Serial.available()) 
  {
    input = Serial.readStringUntil('!');
    velocity = input.toInt();   

    if(input.endsWith("x"))                  //movement in horisontal direction
    {
      if (velocity > 2)
        servo1.write(180, velocity, false);    
      else if (velocity < -2)
        servo1.write(0, -velocity, false);    
      else
      {
        position = servo1.read();
        servo1.write(position, 255, false);       
      } 
    }
    else if(input.endsWith("y"))             //Vertical movement
    {
      if (velocity > 2)
        servo2.write(180, velocity, false);    
      else if (velocity < -2)
        servo2.write(0, -velocity, false);    
      else
      {
        position = servo2.read();
        servo2.write(position, 255, false);       
      } 
    }
    else if(input.endsWith("o"))            //return to origin
    {
      cont++;
      if (cont >= 100)
      {
        position = servo1.read();
        servo1.write(90, 20, true);        
        position = servo2.read();
        servo2.write(70 , 20, true);
        cont = 0;
 
      }
      else
      {
        position = servo1.read();
        servo1.write(position, 255, false);        
        position = servo2.read();
        servo2.write(position, 255, false);
      }
      
            
    }
    input = "";

  }
}
