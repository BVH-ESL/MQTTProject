#!/usr/bin/env python
import sys, os, time
import paho.mqtt.client as mqtt
from serial import Serial
from serial import SerialException
import numpy as np
from matplotlib import pyplot as plt

state           = 0
host            = "10.42.0.48"
port            = 1883
qos             = 0
totalMsg        = 5000
countMsg        = 0
diffTime        = 0
pubTime         = []
subTime         = []
jitterTime      = []
latencyTime     = []
timeList        = []
startTime       = 0
lastMsgTime     = time.time()

#MQTT Functions
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/RPi3/#',qos=qos)

def on_publish(client, userdata, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global lastMsgTime
    global diffTime
    global countMsg
    lastMsgTime = time.time()
    subTime.append(lastMsgTime)
    topics = msg.topic.split("/")
    pubTime.append(float(topics[4]))
    countMsg += 1
    if diffTime == 0:
        diffTime = startTime - pubTime[0]
        print diffTime

#total time = time received last message - time to start receive message
#total message = total messages received
#Throughput = messages received - messages error / total time
def show_report():
    # global msgCount
    print "total time "+str(lastMsgTime-startTime)
    print "total message "+str(countMsg)
    print "Throughput "+str(countMsg/(lastMsgTime-startTime))
    sumLantency = 0
    sumJitter   = 0
    # print len(subTime)
    for i in range(len(pubTime)):
        timeList.append(i)
        currentLantency = subTime[i] - (pubTime[i] + diffTime)
        latencyTime.append(currentLantency)
        sumLantency += currentLantency
        if i != 0:
            # timeList.append(i)
            currentJitter = currentLantency - (subTime[i-1] - (pubTime[i-1] + diffTime))
            sumJitter += currentJitter
            jitterTime.append(currentJitter)
        else:
            jitterTime.append(0)
    print "avg Latency " + str(sumLantency/len(pubTime))
    print "avg Jitter " + str(sumJitter/len(pubTime))

def plot():
    print "plot"
    global jitterTime
    global timeList
    global latencyTime
    # print latencyTime
    # plt.xticks(timeList, timeText
    ax_ch2 = plt.subplot(212)
    ax_ch2.set_title('Jitter')
    ax_ch2.set_xlabel('')
    ax_ch2.set_ylabel('sec')
    ax_ch2.grid(True)
    # plt.plot(timeList, jitterTime)
    markerline, stemlines, baseline = plt.stem(timeList, jitterTime, '-.')

    ax_ch1 = plt.subplot(211, sharex=ax_ch2)
    ax_ch1.set_title('Latency')
    ax_ch1.set_xlabel('')
    ax_ch1.set_ylabel('sec')
    ax_ch1.grid(True)
    plt.plot(timeList, latencyTime)
    plt.show()

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True, protocol=mqtt.MQTTv31)
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
                startTime   = time.time()
                print startTime
                print "Start"
                lastMsgTime = time.time()
                state = 1
        elif state == 1:
            while time.time() - lastMsgTime < 30:
                if countMsg < totalMsg:
                    if countMsg % 100 == 0:
                        pass
                        # print "waiting for " + str(totalMsg - countMsg)
                else:
                    break
            show_report()
            plot()
            break

except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
