#!/usr/bin/env python
import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import threading

class myThread (threading.Thread):
    def __init__(self, threadID, payload, msgcount, delay):
        threading.Thread.__init__(self)
        self.threadID    = threadID
        self.payload     = payload
        self.msgcount    = msgcount
        self.delay       = delay
        # print type(self.threadID)
    def run(self):
        print "Starting " + self.threadID
        # Get lock to synchronize threads
        # threadLock.acquire()
        send_pub(self.threadID, self.payload, int(self.msgcount), delay)
        # Free lock to release next thread
        # threadLock.release()

def send_pub(threadID, payload, msgcount, delay):
    global qos
    cnt = 1
    while cnt <= msgcount:
        # print cnt
        (result,mid)=client.publish('/RPi3/'+str(threadID),payload,qos=qos)
        cnt = cnt+1
        if(cnt % 3000 == 0):
            print str(threadID)+str(cnt)
        time.sleep(delay)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-H", "--host", default="10.42.0.56",
    help="MQTT host to connect to")
ap.add_argument(
    "-P", "--port", type=int, default=1883,
    help="Port for remote MQTT host")
ap.add_argument(
    "-Q", "--qos", type=int, default=1,
    help="Port for remote MQTT host")
ap.add_argument(
    "-M", "--msgcount", type=int, default=10,
    help="Port for remote MQTT host")
ap.add_argument(
    "-p", "--processcount", type=int, default=1,
    help="Port for remote MQTT host")
ap.add_argument(
    "-s", "--payloadsize", type=int, default=2,
    help="Port for remote MQTT host")
ap.add_argument(
    "-T", "--msgpersec", type=float, default=1,
    help="Port for remote MQTT host")
args = vars(ap.parse_args())

host            = args["host"]
port            = args["port"]
qos             = args["qos"]
msgcount        = args["msgcount"]
processcount    = args["processcount"]
payloadsize     = args["payloadsize"]
msgpersec       = args["msgpersec"]

payload         = 'x' * payloadsize

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

def on_publish(client, userdata, mid):
    pass

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# connect to 'localhost', port 1883
# client.connect( "10.42.0.56", 1883, 300 )
client.connect( host, port, 360 )
client.loop_start()

try:
    # threadLock = threading.Lock()
    threads = []
    # thread = []
    # Create new threads
    for i in range(processcount):
        # print i
        # delay = 1/msgpersec/processcount
        delay = 1/msgpersec
        thread = myThread(str(i), payload, msgcount, delay)
        threads.append(thread)
        thread.start()
        # threads[i].start()
    for t in threads:
        t.join()
    print "Exiting Main Thread"
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
