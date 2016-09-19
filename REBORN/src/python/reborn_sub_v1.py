import argparse
import urllib, json
import sys, os, time
import paho.mqtt.client as mqtt
from serial import Serial
from serial import SerialException

ap = argparse.ArgumentParser()
ap.add_argument(
    "-H", "--host", default="10.42.0.48",
    help="MQTT host to connect to")
ap.add_argument(
    "-Q", "--qos", type=int, default=0,
    help="QoS Level")
args = vars(ap.parse_args())

host        = args["host"]
port        = 1883
qos         = args["qos"]
state       = 0
startTime   = 0
lastMsgTime = time.time()
activePub   = 0
pubTime     = []
subTime     = []
currentList = []
voltageList = []
powerList   = []
msgList     = [[]]


def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/RPi3/#',qos=qos)

def on_publish(client, userdata, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global lastMsgTime
    lastMsgTime = time.time()
    global activePub
    global state
    topics = msg.topic.split("/")
    if topics[2] == "ack":
        activePub += 1
        # state =

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv311)
## set callback functions
client.on_connect   = on_connect
client.on_publish   = on_publish
client.on_subscribe = on_subscribe
client.on_message   = on_message
# connect to 'localhost', port 1883
client.connect( host, port, 60 )
client.loop_start()

## specify your serial port here !!!
com_port = '/dev/ttyUSB0'
    # for Ubuntu: use '/dev/ttyUSB0' or '/dev/ttyACM0'
## specify baudrate !!!!
baudrate = 921600
timeout = 1.0
try:
    ser = Serial( port=com_port, baudrate=baudrate, timeout=timeout,
                  bytesize=8, parity='N', stopbits=1 )
except SerialException as ex:
    print ex
    sys.exit(-1)

try:
    while 1:
        if state == 0:
            y = ser.readline()
            if y is None or len(y) == 0:
                continue
            else:
                if y == 'p':
                    state = 1
                elif y == 's':
                    state = 3
        elif state == 1:
            (result,mid)=client.publish('/SUB/check/','',qos=qos)
            state = 2
            time.sleep(5)
            ser.write("r")
        elif state == 2:
            msgList = [[5000]]
        elif state == 3:
            y = ser.readline()

            if y is None or len(y) == 0:
               continue

            datas   = (y.split(","))
            currentlist.append(float(datas[0]))
            voltagelist.append(float(datas[1])/1000)
            powerlist.append(float(datas[0])*(float(datas[1])/1000))

except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    # client.loop_stop()
    # client.disconnect()
    sys.exit(0)
