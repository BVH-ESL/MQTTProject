#!/usr/bin/env python

import sys, time
import paho.mqtt.client as mqtt

# global count
start_time = 0
current_time = 0
time_out = 5
count = 0


### define callback functions for MQTT acctions

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('/#',qos=0)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+ str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global count
    global start_time
    global current_time
    if count == 0:
        start_time = time.time()
        current_time = time.time()
    else:
        current_time = time.time()
    count += 1
    # print count

## create MQTT client
client = mqtt.Client(client_id='',clean_session=True, protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect   = on_connect
client.on_message   = on_message
client.on_subscribe = on_subscribe

# connect to 'localhost', port 1883
client.connect( "10.42.0.56", 1883, 5 )
client.loop_start()

try:
    # print "ready"
    # global count
    while 1: # repeat 10 times
        if count != 0:
            # print ".",
            if time.time() - current_time > 1:
                print " "
                print current_time-start_time
                print count
                current_time = time.time()
                # print current_time
                count = 0
       #time.sleep(2.0) # sleep for 2 seconds
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)


#####################################################################
