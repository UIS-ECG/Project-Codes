/****************************************************************************** 
Heart_Rate_Display over Bluetooth 
Publisher: https://www.circuitschools.com 
******************************************************************************/
#include "ThingSpeak.h"
#include "WiFi.h"

String s_tempA= "6";
String controlledVars[] = {s_tempA};
String cad;
int dato=0;

const char* ssid="Bambam";
const char* password = ".DovalesGalvis9522";
unsigned long channelID=1383805;
const char* WriteAPIKey = "R4E3Y4NW3QZI2MM9";
WiFiClient Client; 

void setup() {
  // initialize the serial communication:
  Serial.begin(9600);
  Serial.println(); // blank line in serial ...
  WiFi.begin(ssid,password);
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("Wifi conectado!");
  ThingSpeak.begin(Client);
  pinMode(41, INPUT); // Setup for leads off detection LO +
  pinMode(40, INPUT); // Setup for leads off detection LO -
  

}
 
void loop() {
  if((digitalRead(40) == 1)||(digitalRead(41) == 1)){
    Serial.println('!');
  }
  else{
    // send the value of analog input 0 to serial:
    Serial.println(analogRead(A0));
  }
  ProcessMsg();
  //Wait a little to keep serial data from saturating

}
void ProcessMsg(){
  if(Serial.available()){
    cad=Serial.readString();
    dato = cad.toInt();
    Serial.println(cad);
    Serial.println(dato+1);
    //digitalWrite(PIN_LED,dato);
    s_tempA = dato;//controlledVars[0];
    ThingSpeak.setField (1, String (s_tempA));
    ThingSpeak.writeFields (channelID, WriteAPIKey);
    delay(20000);
  }
}
