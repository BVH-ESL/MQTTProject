import microgear.client as microgear
import time
import logging

appid = "testNetpie"
gearkey = "TYSjnUASnt3xb5s"
gearsecret =  "QJmJp0lXHDavim4KXvHItE8ez"

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})

def connection():
    logging.debug("Now I am connected with netpie")

def subscription(topic,message):
    logging.debug(topic+" "+message)

def disconnect():
	logging.debug("disconnect is work")

microgear.setalias("testNetpie")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
# microgear.subscribe("/mails")
microgear.connect(False)

while True:
    microgear.chat("testNetpie","Hello world."+str(int(time.time())))
    time.sleep(2)
