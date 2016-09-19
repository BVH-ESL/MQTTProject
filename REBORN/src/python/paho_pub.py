#!/usr/bin/env python
import argparse
import sys, os, time, datetime
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butPin = 17
GPIO.setup(butPin, GPIO.IN)

ap = argparse.ArgumentParser()
ap.add_argument(
    "-rpid", "--rpid", default="1",
    help="RPi Id for publish")
ap.add_argument(
    "-Q", "--qos", type=int, default=0,
    help="QoS Level for transmition")
ap.add_argument(
    "-H", "--host", default="10.42.0.48",
    help="MQTT host to connect to")
ap.add_argument(
    "-d", "--delay", type=float, default=0.01,
    help="delay per msg for transmition")
ap.add_argument(
    "-c", "--connrate", type=int, default=10,
    help="number msg to send in sec")
args = vars(ap.parse_args())

rpiId           = args["rpid"]
qos             = args["qos"]
host            = args["host"]
connRate        = args["connrate"]
delay           = float(1.0/connRate)
payloadSize     = 2
totalMsg        = 5000
state           = 0

def on_connect(client, userdata, flags, rc):
    global qos
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/SUB/#',qos=qos)

def on_publish(client, userdata, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    pass

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv31)

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message   = on_message
client.on_subscribe = on_subscribe

client.connect( host, 1883, 60 )
client.loop_start()
print connRate
print GPIO.input(butPin)
try:
    while 1:
        if state == 0:
            if GPIO.input(butPin) == 0:
                state = 1
        elif state == 1:
            time.sleep(1.2)
            print "start"
            msg = 'a'*payloadSize
            # start = time.time()
            for i in range(totalMsg):
                (result,mid)=client.publish('/RPi3/pub/'+rpiId+'/'+str(time.time()), msg, qos=qos)
                time.sleep(delay)
            break
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
