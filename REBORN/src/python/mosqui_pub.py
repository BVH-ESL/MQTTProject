import argparse
import sys, os, time, datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butPin = 17
GPIO.setup(butPin, GPIO.IN)

ap = argparse.ArgumentParser()
ap.add_argument(
    "-rpid", "--rpid", default="1",
    help="RPi Id for publish")
ap.add_argument(
    "-Q", "--qos", type=int, default=0,
    help="QoS Level for transmition")
ap.add_argument(
    "-H", "--host", default="10.42.0.48",
    help="MQTT host to connect to")
ap.add_argument(
    "-d", "--delay", type=float, default=0.01,
    help="delay per msg for transmition")
ap.add_argument(
    "-c", "--connrate", type=int, default=10,
    help="delay per msg for transmition")
args = vars(ap.parse_args())

rpiId           = args["rpid"]
qos             = args["qos"]
host            = args["host"]
connRate        = args["connrate"]
delay           = float(1.0/connRate)
port            = 1883
payloadSize     = 2
totalMsg        = 5000
state           = 0
print "begin"
print GPIO.input(butPin)
try:
    while 1:
        if state == 0:
            # print GPIO.input(butPin)
            if GPIO.input(butPin) == 0:
                print "press"
                state = 1
        elif state == 1:
            time.sleep(1.2)
            print "start"
            msg = 'a'*payloadSize
            for i in range(totalMsg):
                topic = '/RPi3/pub/'+rpiId+'/'+str(time.time())
                os.popen('mosquitto_pub -h '+host+' -p '+str(port)+' -q '+str(qos)+' -m '+msg+' -t '+topic)
                time.sleep(delay)
            break
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    # client.loop_stop()
    # client.disconnect()
    sys.exit(0)
