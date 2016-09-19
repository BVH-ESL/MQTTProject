import argparse
import time, datetime
import threading, sys, os

ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

host = "192.168.1.1"
port = 1883
qos = 0
totalMsg = 5000
topic = "test/"
msg = "1234"

for i in range(totalMsg):
    os.popen('mosquitto_pub -h '+host+' -p '+str(port)+' -q '+str(qos)+' -m '+msg+' -t '+topic)
    time.sleep(0.01)
