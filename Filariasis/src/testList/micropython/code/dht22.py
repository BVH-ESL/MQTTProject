import dht
import machine
import time

# pin D1
dhtValue = dht.DHT22(machine.Pin(4))
# print
while 1:
    dhtValue.measure()
    print ("Data temp : "+str(dhtValue.temperature())+" humidity : "+str(dhtValue.humidity()))
    time.sleep(1)
