// this code testing read data form DHT22
// ,send it into MQTT Broker
// and setting ESP to Deep sleep mode for 2 seconds
// then repate process again
extern "C" {
#include "user_interface.h"
}
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "DHT.h"

#define processPin 2 // D4

#define DHTPIN 4 // D2 pin to DHT22 data pin
#define DHTTYPE DHT22
char DHTbuff [32];

const char *ssid =	"ESL_Lab1";		// cannot be longer than 32 characters!
const char *pass =	"wifi@esl";		//

// IPAddress of MQTT broker
IPAddress server(192, 168, 1, 183);

// create pubsub client
WiFiClient wclient;
PubSubClient client(wclient, server);

// create dht object
DHT dht(DHTPIN, DHTTYPE);

void setup(){
  Serial.begin(115200);
  Serial.println();
  pinMode(processPin, OUTPUT);
  digitalWrite(processPin, HIGH);
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, pass);
    if (WiFi.waitForConnectResult() != WL_CONNECTED)
      return;
    // Serial.println("WiFi connected");
  }
  digitalWrite(processPin, LOW);
  dht.begin();
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  sprintf(DHTbuff, "%3d.%02d,%3d.%02d", (int)h, (int)(h*100)%100, (int)t, (int)(t*100)%100);
  // Serial.println(DHTbuff);
  digitalWrite(processPin, HIGH);
  if (WiFi.status() == WL_CONNECTED) {
    if (!client.connected()) {
      if (client.connect("arduinoClient")) {
      	client.publish("outTopic",DHTbuff);
  //	client.subscribe("inTopic");
      }
    }
  }
  digitalWrite(processPin, LOW);
  // Take esp into deepSleep Mode for 2 seconds
  ESP.deepSleep(5000000, WAKE_RF_DEFAULT);
}

void loop(){

}
