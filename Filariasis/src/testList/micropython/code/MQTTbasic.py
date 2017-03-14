import network
import time
import machine
import ubinascii
import gc
from umqtt.simple import MQTTClient
from machine import Pin


# Many ESP8266 boards have active-low "flash" button on GPIO0.
# button = Pin(0, Pin.IN)

# Default MQTT server to connect to
SERVER = "192.168.1.183"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"led"

#
# connect the ESP8266 to local wifi network
#
yourWifiSSID = "ESL_Lab1"
yourWifiPassword = "wifi@esl"
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(yourWifiSSID, yourWifiPassword)
print ("connect")

# def main():
c = MQTTClient(CLIENT_ID, SERVER)
c.connect()
# print("Connected to %s, waiting for button presses" % SERVER)
while True:
    c.publish(TOPIC, b"toggle")
    time.sleep(5)

# if __name__ == '__main__':
#     # load_config()
#     # setup_pins()
#     main()
