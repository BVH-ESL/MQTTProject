import machine, dht, time, ubinascii, network
from umqtt.simple import MQTTClient
import gc

# Default MQTT server to connect to
SERVER = "192.168.1.183"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"outTopic"

def set_deepSleep(millisec):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, millisec)
    machine.deepsleep()
# def read
class METHOD:
    def __init__(self):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            # print('connecting to network...')
            sta_if.active(True)
            sta_if.connect('ESL_Lab1', 'wifi@esl')
            while not sta_if.isconnected():
                pass
            # print('network config:', sta_if.ifconfig())

    def activateDeepSleep(self, value, millisec):
        # print (millisec)
        if value:
            c = MQTTClient(CLIENT_ID, SERVER)
            c.connect()
            dhtValue = dht.DHT22(machine.Pin(4))
            dhtValue.measure()
            c.publish(TOPIC, b""+str(dhtValue.temperature())+","+str(dhtValue.humidity()))
            time.sleep(3)
            # print ("Data temp : "+str(dhtValue.temperature())+" humidity : "+str(dhtValue.humidity()))
            set_deepSleep(millisec)
