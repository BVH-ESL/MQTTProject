#!/usr/bin/env python
import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import thread

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ps", "--payloadsize", required = True, help = "payloadsize")
ap.add_argument("-n", "--numpub", required = True, help = "numpub")
ap.add_argument("-l", "--numloop", required = True, help = "numloop")
args = vars(ap.parse_args())

numpub = int(args["numpub"])
payloadsize = int(args["payloadsize"])
numloop = int(args["numloop"])

payload = "x" * payloadsize

# print payload
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_publish(client, userdata, mid):
    pass

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish

## connect to MQTT broker, localhost on port 1883
client.connect( "10.42.0.56", 1883, 300 )
client.loop_start()

def sendpub():
    cnt = 1
    global numpub
    global payload
    while cnt <= numpub:
        (result,mid)=client.publish('/RPi3/1/'+str(time.time()),payload,qos=1)
        cnt = cnt+1
        time.sleep(1)
try:
    sendpub()
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
