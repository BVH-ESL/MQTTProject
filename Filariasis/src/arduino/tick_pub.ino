/*
 Large publish message MQTT example

  - connects to an MQTT server
  - publishes a large string of text to the topic "outTopic"
*/
extern "C" {
#include "user_interface.h"
}
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

const char *ssid =	"Pi_AP";		// cannot be longer than 32 characters!
const char *pass =	"Raspberry";		//

// Update these with values suitable for your network.
IPAddress server(192, 168, 42, 1);

WiFiClient wclient;
PubSubClient client(wclient, server);

void setup() {
  // Setup console
  Serial.begin(115200);
  delay(10);
  Serial.println();
  Serial.println();
}

bool write_payload(Client& payload_stream) {
  char buf[64];
  memset(buf, 32, 64);
  for (int l = 0; l < 1024; l++) {
    int len = sprintf(buf, "%d", l);
    buf[len] = 32;
    buf[63] = '\n';
    uint32_t sent = payload_stream.write((const uint8_t*)buf, 64);
    if (sent < 64)
      return false;
  }
  Serial.println("Published large message.");
  return true;
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.print(ssid);
    Serial.println("...");
    WiFi.begin(ssid, pass);

    if (WiFi.waitForConnectResult() != WL_CONNECTED)
      return;
    Serial.println("WiFi connected");
  }

  if (WiFi.status() == WL_CONNECTED) {
    if (!client.connected()) {
      if (client.connect("arduinoClient")) {
	      client.publish("outTopic", write_payload, 65536);
      }
    }

    if (client.connected())
      client.loop();
  }
}
