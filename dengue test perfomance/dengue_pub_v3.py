#!/usr/bin/env python
import argparse
import sys, os, time, datetime
import paho.mqtt.client as mqtt
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butPin = 17
GPIO.setup(butPin, GPIO.IN)
checkstart = False

ap = argparse.ArgumentParser()
ap.add_argument(
    "-rpid", "--rpid", default="1",
    help="MQTT host to connect to")
ap.add_argument(
    "-Q", "--qos", type=int, default=0,
    help="Port for remote MQTT host")
ap.add_argument(
    "-H", "--host", default="10.42.0.57",
    help="MQTT host to connect to")
args = vars(ap.parse_args())

rpi_id          = args["rpid"]
host            = args["host"]
# rpi_id = "3"
state           = 1
connrate        = 1
payloadsize     = 2
qos             = args["qos"]
processcount    = 10
diftime         = 0
# check_mid       = [[]]
check_mid       = 0
start_time = 0

class myThread (threading.Thread):
    def __init__(self, threadID, payload, msgcount, delay, rpi_id):
        threading.Thread.__init__(self)
        self.threadID    = threadID
        self.payload     = payload
        self.msgcount    = msgcount
        self.delay       = delay
        # print type(self.threadID)
    def run(self):
        # print "Starting " + self.threadID
        send_pub(self.threadID, self.payload, int(self.msgcount), delay, rpi_id)

def send_pub(threadID, payload, msgcount, delay, rpi_id):
    global qos
    global start_time
    global client
    cnt = 1
    while cnt <= msgcount:
        # print time.time()+diftime
        (result,mid)=client.publish('/RPi3/pub/'+rpi_id+'/'+str(threadID)+'/'+str(time.time()-start_time),payload,qos=qos)
        cnt = cnt+1
        if(cnt % 3000 == 0):
            print str(threadID)+str(cnt)
        time.sleep(delay)

def on_connect(client, userdata, flags, rc):
    global qos
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/SUB/#',qos=qos)

def on_publish(client, userdata, mid):
    # global check_mid
    # check_mid+=1
    # print ('Published: ' + str((mid)))
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global state
    global connrate
    global payloadsize
    global processcount
    global diftime
    print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    topics = msg.topic.split("/")
    if topics[2] == "check":
        state = 2
        pass
    if topics[2] == "start":
        payloadsize = int(topics[3])
        connrate = float(topics[4])
        processcount = float(msg.payload)
        # diftime = subtime - time.time()
        # print diftime
        # print time.time() + diftime
        print "waiting for press button"
        state = 4
        # pass

def send_ack():
    global state
    global rpi_id
    global qos
    (result,mid)=client.publish('/RPi3/ack/'+str(rpi_id),'',qos=qos)

# name_pub = "pub"+str(rpi_id)
## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message   = on_message
client.on_subscribe = on_subscribe

client.connect( host, 1883, 60 )
client.loop_start()

try:
    while 1:
        if state == 1:
            # print "waiting for check"
            pass
        elif state == 4:
            if GPIO.input(butPin) == 0:
                state = 3
        elif state == 2:
            time.sleep(0.2)
            send_ack()
            state = 1
        elif state == 3:
            print "start"
            threads = []
            payload = 'x' * payloadsize
            msgcount = connrate*300
            start_time = time.time()
            # print msgcount
            # thread = []
            # Create new threads
            # state = 1
            # check_mid = [[] for x in range(processcount)]
            for i in range(int(processcount)):
                # print i
                # delay = 1/msgpersec/processcount
                delay = 1.0/connrate
                # print delay
                thread = myThread(str(i), payload, msgcount, delay, rpi_id)
                threads.append(thread)
                thread.start()
                # threads[i].start()
            for t in threads:
                t.join()
            print "Exiting Main Thread"
            print check_mid
            state = 1
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
