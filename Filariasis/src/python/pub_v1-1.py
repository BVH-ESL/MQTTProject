import machine, dht, time, ubinascii, network
from umqtt.simple import MQTTClient
import gc

# Default MQTT server to connect to
SERVER = "192.168.1.183"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"outTopic"

def main():
    btn = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
    led = machine.Pin(2, machine.Pin.OUT) #D4
    if btn.value():
        led.value(1)
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            sta_if.active(True)
            sta_if.connect('ESL_Lab1', 'wifi@esl')
            while not sta_if.isconnected():
                pass
            led.value(0)
            dhtValue = dht.DHT22(machine.Pin(4))
            dhtValue.measure()
            led.value(1)
            c = MQTTClient(CLIENT_ID, SERVER)
            c.connect()
            DHTbuff = "%.2f,%.2f" % (dhtValue.humidity(), dhtValue.temperature())
            c.publish(TOPIC, DHTbuff)
            led.value(0)
            time.sleep(3)
            # print ("Data temp : "+str(dhtValue.temperature())+" humidity : "+str(dhtValue.humidity()))
            rtc = machine.RTC()
            rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
            rtc.alarm(rtc.ALARM0, 2000)
            machine.deepsleep()

if __name__ == '__main__':
    main()
