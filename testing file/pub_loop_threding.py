#!/usr/bin/python

import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import threading

class myThread (threading.Thread):
    def __init__(self, threadID, payload, numpub, payloadsize):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.payload = payload
        self.numpub = numpub
        self.payloadsize = payloadsize
        # print type(self.threadID)
    def run(self):
        print "Starting " + self.threadID
        # Get lock to synchronize threads
        threadLock.acquire(1)
        send_pub(str(self.payloadsize), self.payload, int(self.numpub))
        # Free lock to release next thread
        threadLock.release()

def send_pub(channel, payload, numpub):
    cnt = 1
    while cnt <= numpub:
        (result,mid)=client.publish('/test/'+channel,payload,qos=0)
        cnt = cnt+1

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-ps", "--payloadsize", required = True, help = "payloadsize")
ap.add_argument("-np", "--numpub", required = True, help = "numpub")
ap.add_argument("-nt", "--numthred", required = True, help = "numthred")
args = vars(ap.parse_args())

numpub = int(args["numpub"])
# payloadsize = int(args["payloadsize"])
numthred = int(args["numthred"])

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
    payloadsize = [2, 4, 8, 16, 32]
    # payloadsize = [2]
    for x in payloadsize:
        print x
        payload = 'x'*x
        # print payload

        threadLock = threading.Lock()
        threads = []
        for y in range(10):
        # Create new threads
            for i in range(numthred):
                thread = myThread(str(i), payload, numpub, x)
                thread.start()
                threads.append(thread)
                time.sleep(0.25)
            for t in threads:
                t.join()
            print "Exiting Main Thread"
            time.sleep(10)
        print " "
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
