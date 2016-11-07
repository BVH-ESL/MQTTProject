#!/usr/bin/env python
import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import threading
import numpy as np
from matplotlib import pyplot as plt
from serial import Serial
from serial import SerialException

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-H", "--host", default="10.42.0.48",
    help="MQTT host to connect to")
ap.add_argument(
    "-P", "--port", type=int, default=1883,
    help="Port for remote MQTT host")
ap.add_argument(
    "-Q", "--qos", type=int, default=0,
    help="QoS Level")
ap.add_argument(
    "-M", "--msgcount", type=int, default=10,
    help="Total message")
ap.add_argument(
    "-N", "--processcount", type=int, default=10,
    help="Number of Publish")
ap.add_argument(
    "-C", "--connrate", type=int, default=1,
    help="Total connection rate")
ap.add_argument(
    "-s", "--payloadsize", type=int, default=2,
    help="Payload Size of MQTT")
ap.add_argument(
    "-S", "--simtime", type=int, default=300,
    help="Simulation time")
args = vars(ap.parse_args())

host            = args["host"]
port            = args["port"]
qos             = args["qos"]
msgCount        = args["msgcount"]
processCount    = args["processcount"]
conectionRate   = args["connrate"]
payloadSize     = args["payloadsize"]
simulationtime  = args["simtime"]
state           = 1                     #state of program
activepub       = 0
starttime       = 0
lastmsgtime     = time.time()
pubtimelist     = [[]]
subtimelist     = [[]]
checkpacketlist = [[]]
difttimelist    = [[]]
flighttimelist  = [[]]
voltagelist     = []
currentlist     = []
powerlist       = []

#MQTT Functions
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/RPi3/#',qos=qos)

def on_publish(client, userdata, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global lastmsgtime
    lastmsgtime = time.time()
    global state
    global activepub
    topics = msg.topic.split("/")
    if topics[2] == "ack":
        print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        activepub += 1
        state = 2
    else:
        if checkpacketlist[int(topics[3])-1][int(topics[4])] > 0:
            pubtime = float(topics[5])
            if difttimelist[int(topics[3])-1][int(topics[4])] == 0:
                difttimelist[int(topics[3])-1][int(topics[4])] = starttime - pubtime
            pubtimelist[int(topics[3])-1][int(topics[4])].append(pubtime)
            subtimelist[int(topics[3])-1][int(topics[4])].append(lastmsgtime)
            checkpacketlist[int(topics[3])-1][int(topics[4])] -= 1

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

def show_report():
    global totalmsgcount
    global lastmsgtime
    global starttime
    global activepub
    global checkpacketlist
    global processCount
    global pubtimelist
    global subtimelist
    global difttimelist
    checkcount  = 0
    for i in range(activepub):
        checkcount += sum(checkpacketlist[i])
    print "total time "+str(lastmsgtime-starttime)
    print "total message "+str(totalmsgcount-checkcount)
    print "message per seconds "+str((totalmsgcount-checkcount)/(lastmsgtime-starttime)*1)
    calFlightTime()

def calFlightTime():
    global activepub
    global processCount
    global pubtimelist
    global subtimelist
    global difttimelist
    flighttimelist = []
    flighttimeAvglist = []
    for i in range(activepub):
        for j in range(processCount):
            flighttimemin = 9000
            flighttimemax = 0
            flighttimeavg = 0
            for k in range(len(pubtimelist[i][j])):
                flighttimecurrent = subtimelist[i][j][k] - (pubtimelist[i][j][k] + difttimelist[i][j])
                flighttimeavg += flighttimecurrent

                if flighttimecurrent < flighttimemin:
                    flighttimemin = flighttimecurrent

                if flighttimecurrent > flighttimemax:
                    flighttimemax = flighttimecurrent
            flighttime = subtimelist[i][j][len(subtimelist[i][j])-1] - (pubtimelist[i][j][0] + difttimelist[i][j])
            flighttimelist.append(flighttime)
            flighttimeAvglist.append(flighttimeavg/len(subtimelist[i][j]))
    print "total flight time "+str(sum(flighttimelist)/len(flighttimelist))
    print "avg Flight time " +str(sum(flighttimeAvglist)/len(flighttimeAvglist))

def plotFlightTime():
    global pubtimelist

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
        # check active publisher
        if state == 1:
            (result,mid)=client.publish('/SUB/check/','',qos=qos)
            state = 2
            time.sleep(5)
        elif state == 2:
            pubtimelist     = [[[] for x in range(processCount)] for y in range(activepub)]
            subtimelist     = [[[] for x in range(processCount)] for y in range(activepub)]
            # flighttimelist  = [[[] for x in range(processCount)] for y in range(activepub)]
            difttimelist    = [[ 0 for x in range(processCount)] for y in range(activepub)]
            totalmsgcount   = conectionRate*simulationtime
            # print float((totalmsgcount/float(processCount))/activepub)
            checkpacketlist = [[ float((totalmsgcount/float(processCount))/activepub) for x in range(processCount)] for y in range(activepub)]
            (result,mid)    = client.publish('/SUB/start/'+str(payloadSize)+'/'+str(float((conectionRate/float(processCount))/activepub)),str(simulationtime),qos=qos)
            print "waiting for press button"
            state = 3
        elif state == 3 :
            y = ser.readline()
            lastmsgtime = time.time()
            # print y
            if y is None or len(y) == 0:
               continue
            else:
                if starttime == 0:
                    starttime   = time.time()
                print "Start"
                lastmsgtime = time.time()
                state = 4
        elif state == 4:
            while time.time() - lastmsgtime < 30:
                y = ser.readline()

                if y is None or len(y) == 0:
                   continue

                datas   = (y.split(","))
                currentlist.append(float(datas[0]))
                voltagelist.append(float(datas[1])/1000)
                powerlist.append(float(datas[0])*(float(datas[1])/1000))
                checkcount  = 0
                for i in range(activepub):
                    checkcount += sum(checkpacketlist[i])
                if checkcount > 0:
                    if (checkcount % conectionRate) == 0:
                        print "waiting for "+str(checkcount)+" messages"
                else:
                    break

            ser.write("5")
            show_report()
            print "Power avg : "+str(sum(powerlist)/len(powerlist))
            print "Voltage avg : "+str(sum(voltagelist)/len(voltagelist))
            print "Current avg : "+str(sum(currentlist)/len(currentlist))
            print "done!!!"
            break

except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
