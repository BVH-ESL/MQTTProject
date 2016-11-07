#!/usr/bin/env python
import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import thread

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-ps", "--payloadsize", help = "payloadsize")
ap.add_argument("-n", "--numpub", required = True, help = "numpub")
# ap.add_argument("-l", "--numloop",  help = "numloop")
args = vars(ap.parse_args())

numpub = int(args["numpub"])
# payloadsize = int(args["payloadsize"])
# numloop = int(args["numloop"])

# payload = "x" * payloadsize
username = "batman1292"
aiokey = "05a8a2ebaae64073ae2a36241b6d0706"
feed_id = 'DemoFeed'
# print payload
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_publish(client, userdata, mid):
    pass

## create MQTT client
client = mqtt.Client()

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.username_pw_set(username, aiokey)
## connect to MQTT broker, localhost on port 1883
client.connect( "io.adafruit.com", 1883, 300 )
client.loop_start()

def sendpub():
    cnt = 1
    global numpub
    global payload
    while cnt <= numpub:
        (result,mid)=client.publish('{0}/feeds/{1}'.format(username, feed_id), cnt, qos=0)
        cnt = cnt+1
        time.sleep(5)
        print cnt
try:
    sendpub()
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
