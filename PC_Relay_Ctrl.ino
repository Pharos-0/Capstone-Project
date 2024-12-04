#include <LiquidCrystal.h>
#include<SoftwareSerial.h>

#define relay1 8
#define relay2 9
#define relay3 10
#define relay4 11



char buff;

SoftwareSerial BT(3,2); // RX, TX




void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
 BT.begin(9600);
 
 
  pinMode(relay1,OUTPUT);
  pinMode(relay2,OUTPUT);
  pinMode(relay3,OUTPUT);
  pinMode(relay4,OUTPUT);
  
 
   
  digitalWrite(relay1,LOW);
  digitalWrite(relay2,LOW);
  digitalWrite(relay3,LOW);
  digitalWrite(relay4,LOW);
  
  
  
      
 }

void loop() {
 
 if (Serial.available())
 {
    buff = Serial.read();
    //lcd.setCursor(0,1);
    if(buff=='A')
    {
    digitalWrite(relay1,HIGH);
    //Serial.println("A Received");
    //lcd.print("Relay 1 ON    ");
    }
    else if (buff=='B')
    {
    digitalWrite(relay1,LOW);
    //Serial.println("B Received");
   // lcd.print("Relay 1 OFF   ");
    }
    else if (buff=='C')
    {
    digitalWrite(relay2,HIGH);
   // Serial.println("C Received");
   // lcd.print("Relay 2 ON     ");
    }
    else if (buff=='D')
    {
    digitalWrite(relay2,LOW);
   // Serial.println("D Received");
   // lcd.print("Relay 2 OFF     ");
    }
   /* else if (buff=='E')
    {
    digitalWrite(relay3,HIGH);
    lcd.print("Relay 3 ON     ");
    }
    else if (buff=='F')
    {
    digitalWrite(relay3,LOW);
    lcd.print("Relay 3 OFF     ");
    }
    else if (buff=='G')
    {
    digitalWrite(relay4,HIGH);
    lcd.print("Relay 4 ON     ");
    }
    else if (buff=='H')
    {
    digitalWrite(relay4,LOW);
    lcd.print("Relay 4 OFF     ");
    }
    else if (buff=='I')
    {
    digitalWrite(relay1,HIGH);
    lcd.print("Relay 5 ON     ");
    }
    else if (buff=='J')
    {
    digitalWrite(relay1,LOW);
    lcd.print("Relay 5 OFF     ");
    }
    else if (buff=='K')
    {
    digitalWrite(relay6,HIGH);
    lcd.print("Relay 6 ON     ");
    }
    else if (buff=='L')
    {
    digitalWrite(relay6,LOW);
    lcd.print("Relay 6 OFF     ");
    }  */
    
 }
    delay(1000);
    
}
