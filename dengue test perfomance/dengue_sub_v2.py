#!/usr/bin/env python
import argparse
import sys, os, time
import paho.mqtt.client as mqtt
import threading

state = 1

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-H", "--host", default="10.42.0.57",
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
    "-N", "--clientcount", type=int, default=10,
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
# totalmsgcount   = 0
starttime       = 0
lastmsgtime     = time.time()
pubtime         = 0
timelist        = [[]]
checkpacketlist = [[]]

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
    global checkpacketlist
    topics = msg.topic.split("/")
    # print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if topics[2] == "ack":
        print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        activepub += 1
        state = 2
    else:
        if checkpacketlist[int(topics[3])-1][int(topics[4])] > 0:
            lastmsgtime = time.time()
            if starttime == 0:
                starttime = time.time()
            # totalmsgcount -= 1
            pubtime = topics[5]
            timelist[int(topics[3])-1][int(topics[4])].append(float(pubtime))
            checkpacketlist[int(topics[3])-1][int(topics[4])] -= 1

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
    global msgcount
    global totalmsgcount
    global starttime
    global checkpacketlist
    global activepub
    checkcount  = 0
    for i in range(activepub):
        checkcount += sum(checkpacketlist[i])
    print "total time "+str(time.time()-starttime)
    print "total message "+str(msgcount-checkcount)
    print "message per seconds "+str((msgcount-checkcount)/(time.time()-starttime)*1)
    # print "time per message "+str(((time.time()-starttime)/(msgcount-totalmsgcount))*1000)+" ms"
    # print "sumList "+str(sum(checkpacketlist))
    calFilghtTime()
    show_report_packet()
    print checkpacketlist

def calFilghtTime():
    global activepub
    global timelist
    time_flight = [[]]
    print "Total Filght time, Min, Max, Avg"
    for i in range(activepub):
        for j in range(clientcount):
            # print len(timelist[i][j])
            time_min = 9000
            time_max = 0
            time_avg = 0
            for k in range(1, len(timelist[i][j])):
                time_current = timelist[i][j][k] - timelist[i][j][k-1]
                time_avg += time_current
                if time_current < time_min:
                    time_min = time_current
                if time_current > time_max:
                    time_max = time_current
            print str(timelist[i][j][len(timelist[i][j])-1]-timelist[i][j][0])+","+str(time_min)+","+str(time_max)+","+str(time_avg/len(timelist[i][j]))
            # time_flight[i][0] = timelist[i][j][len(timelist[i][j])-1]-timelist[i][j][0]
            # time_flight[i][1] = time_min
            # time_flight[i][2] = time_max
            # time_flight[i][3] = time_avg
            # print "RPi ID : "+str(i)+" ThreadID : "+str(y)
def show_report_packet():
    global checkpacketlist
    print checkpacketlist

try:
    while 1:
        if state == 1:
            (result,mid)=client.publish('/SUB/check/','',qos=qos)
            state = 2
            time.sleep(5)
        elif state == 2:
            # pass
            # print activepub
            timelist = [[[] for x in range(clientcount)] for y in range(activepub)]

            # print timelist
            lastmsgtime = time.time()
            msgcount = connrate*300
            # totalmsgcount = connrate*300
            (result,mid)=client.publish('/SUB/start/'+str(payloadsize)+'/'+str(float((connrate/float(clientcount))/activepub)),str(clientcount),qos=qos)
            checkpacketlist = [[ float((msgcount/float(clientcount))/activepub) for x in range(clientcount)] for y in range(activepub)]
            # print sum(checkpacketlist[0])
            state = 3

            # print "waiting for ack"
        else :
            while time.time() - lastmsgtime < 30:
                checkcount  = 0
                for i in range(activepub):
                    checkcount += sum(checkpacketlist[i])
                if checkcount > 0:
                # print time.time() - currenttime
                    # sum1 =
                    # print str(sum(list(checkpacketlist)))
                    print "waiting for "+str(checkcount)+" messages"
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
