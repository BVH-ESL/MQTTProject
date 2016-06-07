#!/usr/bin/env python
import argparse
import sys, os, time
import paho.mqtt.client as mqtt

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
    "-N", "--clientcount", type=int, default=1,
    help="Port for remote MQTT host")
args = vars(ap.parse_args())

host            = args["host"]
port            = args["port"]
qos             = args["qos"]
msgcount        = args["msgcount"]
clientcount     = args["clientcount"]
totalmsgcount   = msgcount*clientcount
timelist        = []
clientlist      = []
starttime       = 0
startprotime    = time.time()
lastmsgtime     = time.time()
# for i in range(clientcount):
#     clientlist[i] = 0

### define callback functions for MQTT acctions
def on_connect(client, userdata, flags, rc):
    global qos
    print("Connected with result code " + str(rc))
    client.subscribe('/#',qos=qos)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+ str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global msgcount
    global clientcount
    global timelist
    global totalmsgcount
    global starttime
    global lastmsgtime
    lastmsgtime = time.time()
    if starttime == 0:
        starttime = time.time()
    # topics = msg.topic.split("/")
    # pubtime = topics[3]
    # timelist.append(time.time()-time.mktime(time.localtime(float(pubtime))))
    totalmsgcount -= 1

def show_report():
    global timelist
    global msgcount
    global clientcount
    global totalmsgcount
    global starttime
    # timemax = max(timelist)
    # timemin = min(timelist)
    # timeavg = sum(timelist)/len(timelist)
    # print "starttime "+str(starttime.strftime("%H:%M:%S"))
    print "stoptime "+time.strftime("%H:%M:%S")
    print "total message "+str(msgcount*clientcount-totalmsgcount)
    print "total time "+str(time.time()-starttime)
    print "message per seconds "+str((msgcount*clientcount-totalmsgcount)/(time.time()-starttime)*1)
    print "time per message "+str(((time.time()-starttime)/(msgcount*clientcount-totalmsgcount))*1000)+" ms"
    # print "Flight time min "+str(timemin*1000)+" ms"
    # print "Flight time max "+str(timemax*1000)+" ms"
    # print "Flight time avg "+str(timeavg*1000)+" ms"

## create MQTT client
client = mqtt.Client(client_id='',clean_session=True, protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect   = on_connect
client.on_message   = on_message
client.on_subscribe = on_subscribe

# connect to 'localhost', port 1883
client.connect( host, port, 360 )
client.loop_start()

try:
    while time.time() - lastmsgtime < 30:
        if totalmsgcount > 0:
        # print time.time() - currenttime
            print "waiting for "+str(totalmsgcount)+" messages"
            time.sleep(1)
        else:
            break
    # print timelist
    show_report()
    print "done"
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
