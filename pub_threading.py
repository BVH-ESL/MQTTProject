#!/usr/bin/python

import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import threading

class myThread (threading.Thread):
    def __init__(self, threadID, payload, numpub):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.payload = payload
        self.numpub = numpub
        # print type(self.threadID)
    def run(self):
        print "Starting " + self.threadID
        # Get lock to synchronize threads
        threadLock.acquire(1)
        send_pub(self.threadID, self.payload, int(self.numpub))
        # Free lock to release next thread
        threadLock.release()

def send_pub(channel, payload, numpub):
    cnt = 1
    while cnt <= numpub:
        (result,mid)=client.publish('/test/'+channel,payload,qos=0)
        cnt = cnt+1

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ps", "--payloadsize", required = True, help = "payloadsize")
ap.add_argument("-np", "--numpub", required = True, help = "numpub")
ap.add_argument("-nt", "--numthred", required = True, help = "numthred")
args = vars(ap.parse_args())

numpub = int(args["numpub"])
payloadsize = int(args["payloadsize"])
numthred = int(args["numthred"])
# print numthred
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


try:
    threadLock = threading.Lock()
    threads = []
    # thread = []
    # Create new threads
    for i in range(numthred):
        # print i
        thread = myThread(str(i), payload, numpub)
        thread.start()
        threads.append(thread)
    # thread1 = myThread(str(1), payload, numpub)
    # thread2 = myThread(str(2), payload, numpub)

    # Start new Threads
    # thread1.start()
    # thread2.start()

    # Add threads to thread list
    # threads.append(thread1)
    # threads.append(thread2)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print "Exiting Main Thread"
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
