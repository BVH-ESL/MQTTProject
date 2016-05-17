#!/usr/bin/env python

import sys, time
import paho.mqtt.client as mqtt

### define callback functions for MQTT acctions

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('/#',qos=1)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+ str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    #print(msg)
    # print(msg.retain)
    #print(userdata)

## create MQTT client
client = mqtt.Client(client_id='',clean_session=True, protocol=mqtt.MQTTv311)

## set callback functions
client.on_connect   = on_connect
client.on_message   = on_message
client.on_subscribe = on_subscribe

# connect to 'localhost', port 1883
client.connect( "10.42.0.56", 1883, 60 )

# loop forever
client.loop_forever()

#####################################################################
