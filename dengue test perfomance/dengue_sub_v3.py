#!/usr/bin/env python
import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import threading

state = 1

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-H", "--host", default="10.42.0.56",
    help="MQTT host to connect to")
ap.add_argument(
    "-P", "--port", type=int, default=1883,
    help="Port for remote MQTT host")
ap.add_argument(
    "-Q", "--qos", type=int, default=0,
    help="Port for remote MQTT host")
ap.add_argument(
    "-M", "--msgcount", type=int, default=10,
    help="Port for remote MQTT host")
ap.add_argument(
    "-N", "--clientcount", type=int, default=1,
    help="Port for remote MQTT host")
ap.add_argument(
    "-C", "--connrate", type=int, default=1,
    help="Port for remote MQTT host")
ap.add_argument(
    "-s", "--payloadsize", type=int, default=2,
    help="Port for remote MQTT host")
args = vars(ap.parse_args())

host            = args["host"]
port            = args["port"]
qos             = args["qos"]
clientcount     = args["clientcount"]
connrate        = args["connrate"]
payloadsize     = args["payloadsize"]
activepub       = 0
msgcount        = 0
totalmsgcount   = 0
starttime       = 0
lastmsgtime     = time.time()
pubtime         = 0
timelist        = [[]]

def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/RPi3/#',qos=qos)

def on_publish(client, userdata, mid):
    # print ('Published: ' + str(mid))
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global state
    global activepub
    global totalmsgcount
    global lastmsgtime
    global starttime
    global timelist
    global pubtime
    # print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    topics = msg.topic.split("/")
    if topics[2] == "ack":
        print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        activepub += 1
        state = 2
    else:
        lastmsgtime = time.time()
        if starttime == 0:
            starttime = time.time()
        totalmsgcount -= 1
        pubtime = topics[5]
        # timelist[int(topics[3])-1][int(topics[4])].append(float(pubtime))
        # print pubtime
        # print time.time()-float(pubtime)
        # timelist.append(time.time()-time.mktime(time.localtime(float(pubtime))))
        # timelist.append(time.time()-float(pubtime))
    # state = 1

def send_check():
    global state
    global qos
    (result,mid)=client.publish('/SUB/check/','',qos=qos)
    state = 2

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message   = on_message

# connect to 'localhost', port 1883
client.connect( host, port, 360 )
client.loop_start()

def show_report():
    global timelist
    global msgcount
    # global clientcount
    global totalmsgcount
    global starttime
    # timemax = max(timelist)
    # timemin = min(timelist)
    # timeavg = sum(timelist)/len(timelist)
    # print "starttime "+str(starttime.strftime("%H:%M:%S"))
    print "stoptime "+time.strftime("%H:%M:%S")
    print "total time "+str(time.time()-starttime)
    print "total message "+str(msgcount-totalmsgcount)
    print "message per seconds "+str((msgcount-totalmsgcount)/(time.time()-starttime)*1)
    print "time per message "+str(((time.time()-starttime)/(msgcount-totalmsgcount))*1000)+" ms"
    # print "Flight time min "+str(timemin*1000)+" ms"
    # print "Flight time max "+str(timemax*1000)+" ms"
    # print "Flight time avg "+str(timeavg*1000)+" ms"
    print timelist


try:
    while 1:
        if state == 1:
            (result,mid)=client.publish('/SUB/check/','',qos=qos)
            state = 2
            time.sleep(5)
        elif state == 2:
            # pass
            # print activepub
            timelist = [[[] for x in range(10)] for y in range(activepub)]
            # print timelist
            lastmsgtime = time.time()
            msgcount = connrate*300
            totalmsgcount = connrate*300
            (result,mid)=client.publish('/SUB/start/'+str(payloadsize)+'/'+str(float((connrate/10.0)/activepub)),str(time.time()),qos=qos)
            state = 3
            # print "waiting for ack"
        else :
            while time.time() - lastmsgtime < 30:
                if totalmsgcount > 0:
                # print time.time() - currenttime
                    print "waiting for "+str(totalmsgcount)+" messages"
                    time.sleep(1)
                else:
                    break
            show_report()
            print "done"
            break
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
