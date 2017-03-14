#include <MicroGear.h>
#include <ESP8266WiFi.h>

// pinMode(startProcessPin, OUTPUT);
// pinMode(pubProcessPin, OUTPUT);
// pinMode(mainProcessPin, OUTPUT);
// digitalWrite(startProcessPin, HIGH);
// digitalWrite(pubProcessPin, HIGH);
// digitalWrite(mainProcessPin, HIGH);

// define wifi ssid and password
const char* SSID = "ESL_Lab1";
const char* PASS = "wifi@esl";

// define NETPI variable for testing
#define APPID   "ESLtestApp"
#define KEY     "shq6OEyVz20rJFd"
#define SECRET  "mYvejkzTfmWanizkulxlsLOaC"
#define ALIAS   "NodeMCUArduino"

// set testing variable
#define mainProcessPin 14            // D5 pin
#define pubProcessPin 12            //D6 pin
#define startProcessPin  13            // D7 pin
#define payloadSize 128            // num payload size
#define testLoop 100              // testing pub loop
char payload [payloadSize];                // dummy payload for testing
int sleepTime = 30;               // setting time to sleep
int state = 0;                    // state of process

// create variable toconnect NETPI
WiFiClient client;
MicroGear microgear(client);

void onMsghandler(char *topic, uint8_t* msg, unsigned int msglen) {
  Serial.print("Incoming message --> ");
  msg[msglen] = '\0';
  Serial.println((char *)msg);
}

void onConnected(char *attribute, uint8_t* msg, unsigned int msglen) {
 // Serial.println("connect");
  microgear.setAlias(ALIAS);
}

void setup(){
  Serial.begin(115200);
  Serial.println();
  pinMode(startProcessPin, OUTPUT);
  pinMode(pubProcessPin, OUTPUT);
  pinMode(mainProcessPin, OUTPUT);
  digitalWrite(startProcessPin, HIGH);
  digitalWrite(pubProcessPin, HIGH);

  // set MQTT callback process
  digitalWrite(mainProcessPin, HIGH);
  microgear.on(MESSAGE,onMsghandler);
  microgear.on(CONNECTED,onConnected);
  delay(50);
  // Serial.print(0);  Serial.println(millis());
  // state++;

  // connect AP process
  digitalWrite(mainProcessPin, LOW);
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(SSID, PASS);
    if (WiFi.waitForConnectResult() != WL_CONNECTED)
      return;
  }
  // Serial.print(1);  Serial.println(millis());
  // state++;

  // create dummy payload process
  digitalWrite(mainProcessPin, HIGH);
  for(int i = 0; i < payloadSize; i++){
    payload[i] = 'x';
  }
  delay(50);
  // Serial.print(2);  Serial.println(millis());
  // state++;

  // connect to broker process
  digitalWrite(mainProcessPin, LOW);
  microgear.init(KEY,SECRET,ALIAS);
  microgear.connect(APPID);
  // Serial.print(3);  Serial.println(millis());
  // state++;

  // testing publisher payload process
  digitalWrite(mainProcessPin, HIGH);
  for(int i = 0; i < testLoop; i++){
    digitalWrite(pubProcessPin, !digitalRead(pubProcessPin));
    if (microgear.connected()){
      while (!microgear.publish("/pub", payload));
    }
    // Serial.print(state);  Serial.println(millis());
    // state++;
  }

  digitalWrite(startProcessPin, LOW);
  digitalWrite(mainProcessPin, LOW);
  digitalWrite(pubProcessPin, !digitalRead(pubProcessPin));
  ESP.deepSleep(15000000ul, WAKE_RF_DEFAULT);
}

void loop(){

}
