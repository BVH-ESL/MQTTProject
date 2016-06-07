#!/usr/bin/env python

import sys, os, time
import paho.mqtt.client as mqtt

### define callback functions

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_publish(client, userdata, mid):
    print ('Published: ' + str(mid))

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish

## connect to MQTT broker, localhost on port 1883
client.connect( "10.42.0.56", 1883, 60 )
client.loop_start()

cnt=1
try:
    while cnt <= 1000: # repeat 10 times
        (result,mid)=client.publish('/test/sample','12345678',qos=1)
        cnt = cnt+1
       #time.sleep(2.0) # sleep for 2 seconds
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
