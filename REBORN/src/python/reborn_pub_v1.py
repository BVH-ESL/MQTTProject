import urllib, json
import sys, os, time, datetime
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butPin = 17
GPIO.setup(butPin, GPIO.IN)

ap = argparse.ArgumentParser()
ap.add_argument(
    "-rpid", "--rpid", default="1",
    help="RPi Id for publish")
args = vars(ap.parse_args())

rpiId           = args["rpid"]
state           = 0
host            = "10.42.0.48"
port            = 1883
keep            = 60
qos             = 0
payloadSizeList = []
payloadSizeindex= 0
msgRateList     = []
msgRate         = 0
msgRateStep     = 0
qosList         = []
msgTotal        = 0

def on_connect(client, userdata, flags, rc):
    global qos
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/SUB/#',qos=qos)

def on_publish(client, userdata, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    topics = msg.topic.split("/")
    if topics[2] == "check":
        time.sleep(0.2)
        send_ack()
        print "wait for start signal"

def send_ack():
    global rpi_id
    global qos
    (result,mid)=client.publish('/RPi3/ack/'+str(rpi_id),'',qos=qos)

## create MQTT client
client = mqtt.Client(client_id="", clean_session=True,protocol=mqtt.MQTTv31)

## set callback functions
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message   = on_message
client.on_subscribe = on_subscribe

client.connect(host, port, keep)
client.loop_start()
try:
    while 1:
        if state == 0:                  # wait for start test signal
            if GPIO.input(butPin) == 0:
                state = 1
        elif state == 1:                # get JSON sequence test data form PC
            url = "http://localhost:3000/jsontest"
            output = json.load(urllib.urlopen(url))
            payloadSizeList = output["payloadsize"]
            msgRateList     = output["msgrate"]
            msgRateStep     = output["steprate"]
            msgTotal        = output["totalmsg"]
            print "wait for check signal"
        elif state == 2:                # wait for scan signal
            if GPIO.input(butPin) == 0:
                state = 3
        elif state == 3:
            if msgRate == 0:
                msgRate = msgRateList[0]
            elif msgRate == msgRateList[1]:
                payloadSizeindex += 1
                msgRate = 0
                if payloadSizeindex == len(payloadSizeList):
                    break
            else:
                msgRate += msgRateStep
            delay = float(1.0/msgRate)
            payload = 'x' * payloadSizeList[payloadSizeindex]
            for i in range(msgTotal):
                (result,mid)=client.publish('/RPi3/pub/'+rpiId+'/'+str(time.time()), payload, qos=qos)
                time.sleep(delay)
            state = 2


except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
