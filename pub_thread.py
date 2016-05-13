#!/usr/bin/env python

import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import thread
# from threading import Thread

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
client.connect( "10.42.0.56", 1883, 60 )
client.loop_start()

# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print "Starting " + self.name
#         print_time(self.name, self.counter, 5)
#         print "Exiting " + self.name


def sendpub(channle, delay):
    print "start"+channle
    cnt = 1
    global numpub
    global payload
    while cnt <= numpub:
        (result,mid)=client.publish('/test/',payload,qos=0)
        cnt = cnt+1
        time.sleep(0.2)
    print "end"+channle

try:
    time.sleep(0.5)
    thread.start_new_thread(sendpub, ("1", 0.5))
    thread.start_new_thread(sendpub, ("2", 0.5))
    thread.start_new_thread(sendpub, ("3", 0.5))
    thread.start_new_thread(sendpub, ("4", 0.5))
    thread.start_new_thread(sendpub, ("5", 0.5))
    thread.start_new_thread(sendpub, ("6", 0.5))
    thread.start_new_thread(sendpub, ("7", 0.5))
    thread.start_new_thread(sendpub, ("8", 0.5))
    thread.start_new_thread(sendpub, ("9", 0.5))
    thread.start_new_thread(sendpub, ("10", 0.5))
    # cnt=1
    # thread1 = Thread(target = sendpub, args = ("10", 12))
    # thread.start()
    # cnt=1
    # thread2 = Thread(target = sendpub, args = ("10", 12))
    # thread.start()
    # thread.join()
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
