import argparse
import sys, os, time, datetime
import paho.mqtt.client as mqtt
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butPin = 17
GPIO.setup(butPin, GPIO.IN)

ap = argparse.ArgumentParser()
ap.add_argument(
    "-rpid", "--rpid", default="1",
    help="RPi Id for publish")
ap.add_argument(
    "-H", "--host", default="10.42.0.27",
    help="MQTT host to connect to")
ap.add_argument(
    "-Q", "--qos", type=int, default=1,
    help="QoS Level")
args = vars(ap.parse_args())

rpi_id      = args["rpid"]
host        = args["host"]
port        = 1883
qos         = args["qos"]
state       = 0
payloadSize = 1
msgRate     = 1
msgTotal    = 0
startTime   = 0
isStart     = 0

class myThread (threading.Thread):
    def __init__(self, threadID, payload, msgcount, delay, rpi_id):
        threading.Thread.__init__(self)
        self.threadID    = threadID
        self.payload     = payload
        self.msgcount    = msgcount
        self.delay       = delay
    def run(self):
        send_pub(self.threadID, self.payload, int(self.msgcount), self.delay, rpi_id)

def send_pub(threadID, payload, msgcount, delay, rpi_id):
    print delay
    global qos
    cnt = 1
    while cnt <= msgcount:
        (result,mid)=client.publish('/RPi3/pub/'+rpi_id+'/'+str(threadID)+'/'+str(time.time()),payload,qos=qos)
        cnt = cnt+1
        time.sleep(delay)


def on_connect(client, userdata, flags, rc):
    global qos
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/SUB/#',qos=qos)

def on_publish(client, userdata, mid):
    # print "sendding"
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global payloadSize
    global msgRate
    global msgTotal
    global rpi_id
    global qos
    print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    topics = msg.topic.split("/")
    if topics[2] == "check":
        (result,mid)=client.publish('/RPi3/ack/'+str(rpi_id),'',qos=qos)
    elif topics[2] == "set":
        # if msgRate != float(topics[4]):
        payloadSize = int(topics[3])
        msgRate     = float(topics[4])
        msgTotal    = float(topics[5])
        # print msgT
        (result,mid)=client.publish('/RPi3/ready/'+str(rpi_id)+'/'+str(msgRate),'',qos=qos)
    # elif topics[2] == "done":
        # state = kdk

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
        if state == 0:
            # print "start"
            if GPIO.input(butPin) == 1:
                state = 1
                # isStart = 0
        elif state == 1:
            # print "start"
            procescount = 10
            threads = []
            payload = 'x' * payloadSize
            # print payload
            for i in range(int(procescount)):
                delay = 1.0/msgRate
                thread = myThread(str(i), payload, msgTotal, delay, rpi_id)
                threads.append(thread)
                thread.start()
            for t in threads:
                t.join()
            print "Exiting Main Thread"
            state = 0
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
