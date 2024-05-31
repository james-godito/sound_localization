
#include <SPI.h>

/*
// Arduino MEGA 2560 R3
#define BUSY 32               // you can use any digital pin   
#define RESET 30              // you can use any digital pin  
#define CVAB 34               // you can use any digital pin    
#define CS 53                 // SPI CS     
#define D7_out 50             // SPI MISO there is no need to use MOSI pin with the ad7606 
#define RD 52                 // SPI SCLK 
*/

// Arduino UNO Wifi
#define BUSY 8   // you can use any digital pin   
#define RESET 9   // you can use any digital pin  
#define CVAB 7   // you can use any digital pin    
#define CS 10     // SPI CS     
#define D7_out 12 // SPI CIPO
#define RD 13     // SPI SCLK

#define scaleFactor 0.00007629394531 // 5V/2^16
#define totalBytes 6 // 2 bytes per channel, 10 bytes for 5 channels
#define channelsUsed 3 // max 8 channels
#define offset 29500

int bytesToRead = totalBytes;
uint8_t raw[totalBytes];
uint16_t parsed[channelsUsed]; // 2 bytes * 8 = 16 bytes total

const char STX = '\x002';
const char ETX = '\x003';





long lastMicros = 0;
long loops = 0;

uint32_t startTime, elapsedTime, old_res;

const int scale1 = 0.00322265625;

void setup()
{
  pinMode(RESET, OUTPUT);
  pinMode(CS, OUTPUT);
  pinMode(CVAB, OUTPUT);
  pinMode(D7_out, OUTPUT);
  pinMode(RD, OUTPUT);
  pinMode(BUSY, INPUT);

  digitalWrite(CS, HIGH);
  digitalWrite(CVAB, HIGH);
  digitalWrite(RESET, 0);
  pulse(RESET);
  
  

  Serial.begin(500000); // change to higher in practice
  SPI.begin();
}

void loop()
{ 
  readData();
  Serial.write(STX);
  Serial.write((byte*)&raw, totalBytes + 1);
  Serial.write(ETX);
  
  
  

  /*
  // used to find how long a function takes to run
  startTime = micros();

  // place function to evaluate here
  
  elapsedTime = micros() - startTime;  

  if (elapsedTime != old_res)
  {
    Serial.print("Elapsed time:\t");
    Serial.print(elapsedTime);
    Serial.println(" microseconds");
    old_res = elapsedTime;
  }
  // ---------------------------------------
  
  // used for spacing reads
  if (currentMicros - lastMicros > 1000000) 
  {
    Serial.print("Elapsed:");
    Serial.println(currentMicros - lastMicros);
    lastMicros = currentMicros;
  }
  
  // for debugging input from mics
  Serial.print(parsed[0]);
  Serial.print(",");
  Serial.print(parsed[1]);
  Serial.print(",");
  Serial.print(parsed[2]);
  Serial.print("\n");
  */
}  

void pulse(uint8_t pin) 
{
  // initiate conversion
  digitalWrite(pin, HIGH);
  digitalWrite(pin, LOW); 
}

void ipulse(uint8_t pin) 
{
  // initiate conversion
  digitalWrite(pin, LOW);
  digitalWrite(pin, HIGH); 
}

void parseRawBytes() 
{
  for (int i = 0; i < (sizeof(parsed) / sizeof(int) * 2); i++) // Depends on MCU, if Arduino Uno Wifi R4 *2 since int is 4 bit
  {
      parsed[i] = (raw[i*2] << 8) + raw[(i*2) + 1];
  }
}

void readData() 
{
  ipulse(CVAB);
  
  while (digitalRead(BUSY) == HIGH) 
  {
  // busy high while converting, low when done 
  }

  SPI.beginTransaction(SPISettings(200000, MSBFIRST, SPI_MODE1)); // Based on AD7606 manual, 200kSPS, MSBF, CPOL = 0, CPHA = 1
  digitalWrite(CS, LOW);

  while (bytesToRead > 0) 
  {
    raw[totalBytes - bytesToRead] = SPI.transfer(0x00);
    bytesToRead--;
  }
  
  digitalWrite(CS, HIGH);
  SPI.endTransaction();

  bytesToRead = totalBytes;
}