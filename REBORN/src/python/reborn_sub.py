import argparse
import urllib, json
import sys, os, time, datetime, csv
import paho.mqtt.client as mqtt
from serial import Serial
from serial import SerialException

ap = argparse.ArgumentParser()
ap.add_argument(
    "-H", "--host", default="10.42.0.83",
    help="MQTT host to connect to")
ap.add_argument(
    "-Q", "--qos", type=int, default=0,
    help="QoS Level")
args = vars(ap.parse_args())

host            = args["host"]
port            = 1883
qos             = args["qos"]
state           = 0
activePub       = 0
activePubList   = []
readyPub        = 0
payloadSizeList = []
payloadSizeindex= 0
msgRateList     = []
msgRate         = 0
msgRateStep     = 0
msgTotal        = 0
startMsgTime    = 0
lastMsgTime     = time.time()
timeOut         = 0
pubtimeList     = [[]]
subtimeList     = [[]]
difttimeList    = [[]]
msgCountList    = [[]]
voltageList     = []
currentList     = []
powerList       = []
avgLatency      = 0
procescount     = 10

#report function
def saveResultFile():
    global payloadSizeList
    global payloadSizeindex
    global msgRate
    global lastMsgTime
    global startMsgTime
    global msgCountList
    global activePub
    global msgTotal
    global avgLatency
    global voltageList
    global currentList
    global powerList

    # print "start save overrall"
    bufferString = ""
    now = datetime.datetime.now()
    txtFileName = "result/overrall"+now.strftime('%m%d%Y-%H')+".txt"
    # fileCount = 0
    # while os.path.exists(txtFileName):
    #     txtFileName = "result/overrall"+now.strftime('%m%d%Y-%H')+str(fileCount)+".txt"
    #     fileCount += 1

    checkcount = 0
    for i in range(activePub):
        checkcount += sum(msgCountList[i])

    payloadSize = payloadSizeList[payloadSizeindex]
    recivedMsg = msgTotal - checkcount
    totalTime = lastMsgTime - startMsgTime
    thoughput = recivedMsg/totalTime

    avgVoltage = sum(voltageList)/len(voltageList)
    avgCurrent = sum(currentList)/len(currentList)
    avgPower   = sum(powerList)/len(powerList)
    bufferString = str(payloadSize)+','+str(msgRate)+','+str(recivedMsg)+','+str(totalTime)+','+str(thoughput)+','+str(avgLatency)+','+str(avgPower)+','+str(avgVoltage)+','+str(avgCurrent)+'\n'
    file = open(txtFileName, "a")
    file.write(bufferString)
    file.close()
    # print "done save overrall"

def saveLatencyFile():
    global payloadSizeList
    global payloadSizeindex
    global msgRate
    global pubtimeList
    global subtimeList
    global difttimeList
    global procescount
    global activePub
    global avgLatency
    avgLatencyList = []
    bufferString = ""
    now = datetime.datetime.now()
    txtFileName = "result/latency"+str(payloadSizeList[payloadSizeindex])+str(msgRate)+"_"+now.strftime('%m%d%Y-%H%M')+".txt"
    file = open(txtFileName, "w")
    for i in range(activePub):
        for j in range(procescount):
            flighttimeavg = 0
            for k in range(len(pubtimeList[i][j])):
                currentLatency = subtimeList[i][j][k] - (pubtimeList[i][j][k] + difttimeList[i][j])
                flighttimeavg += currentLatency
                bufferString += str(currentLatency) + ','
            bufferString += '\n'
            avgLatencyList.append(flighttimeavg/len(pubtimeList[i][j]))
            file.write(bufferString)
            bufferString = ""
    file.close()
    # print "done save latency"
    avgLatency = sum(avgLatencyList)/len(avgLatencyList)

def savePowerConsumtion():
    global voltageList
    global currentList
    global powerList
    bufferString = ""
    now = datetime.datetime.now()
    txtFileName = "result/power"+str(payloadSizeList[payloadSizeindex])+str(msgRate)+"_"+now.strftime('%m%d%Y-%H%M')+".txt"
    file = open(txtFileName, "w")
    for i in range(len(powerList)):
        bufferString = str(powerList[i])+','+str(voltageList[i])+','+str(currentList[i])+'\n'
        file.write(bufferString)
    file.close()
    # print "done save power"

# MQTT Function
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    client.subscribe('/RPi3/#',qos=qos)

def on_publish(client, userdata, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global lastMsgTime
    lastMsgTime = time.time()
    global activePub
    global activePubList
    global readyPub
    global state
    global msgTotal
    global msgCount
    global msgRate
    topics = msg.topic.split("/")
    if topics[2] == "ack":
        print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        activePub += 1
        # state = 2
    elif topics[2] == "ready":
        print("Received:" + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        print float(msgRate/activePub)
        if activePubList[int(topics[3])-1] == 0 and float(topics[4]) == float(msgRate/activePub):
            readyPub += 1
            activePubList[int(topics[3])-1] += 1
        state = 3
    else:
        if msgCountList[int(topics[3])-1][int(topics[4])] > 0:
            pubtime = float(topics[5])
            if difttimeList[int(topics[3])-1][int(topics[4])] == 0:
                difttimeList[int(topics[3])-1][int(topics[4])] = startMsgTime - pubtime
            pubtimeList[int(topics[3])-1][int(topics[4])].append(pubtime)
            subtimeList[int(topics[3])-1][int(topics[4])].append(lastMsgTime)
            msgCountList[int(topics[3])-1][int(topics[4])] -= 1

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
        if state == 0:
            y = ser.readline()
            if y is None or len(y) == 0:
                continue
            else:
                print y
                if y == 'p':
                    state = 1
                elif y == 's':
                    startMsgTime = time.time()
                    lastMsgTime = time.time()
                    state = 4
                    print "start"
                elif y == 'r':
                    state = 2
                else:
                    startMsgTime = time.time()
                    lastMsgTime = time.time()
                    state = 4
                    print "start"
                    print msgRate
        elif state == 1:
            url = "http://localhost:3000/jsontest"
            output = json.load(urllib.urlopen(url))
            print output
            payloadSizeList = output["payloadsize"]
            msgRateList     = output["msgrate"]
            msgRateStep     = output["steprate"]
            msgTotal        = output["totalmsg"]
            timeOut         = output["timeout"]
            # print msgRateList[0]
            (result,mid)=client.publish('/SUB/check/','',qos=qos)
            time.sleep(20)
            state = 2
        elif state == 2:        #prepare state
            # procescount = 10
            # time.sleep(5)
            activePubList   = [0 for x in range(activePub)]
            pubtimeList     = [[[] for x in range(procescount)] for y in range(activePub)]
            subtimeList     = [[[] for x in range(procescount)] for y in range(activePub)]
            difttimeList    = [[ 0 for x in range(procescount)] for y in range(activePub)]
            msgCountList    = [[ float((msgTotal/float(procescount))/activePub) for x in range(procescount)] for y in range(activePub)]
            voltageList     = []
            currentList     = []
            powerList       = []

            if msgRate == 0:
                msgRate = msgRateList[0]
            elif msgRate == msgRateList[1]:
                payloadSizeindex += 1
                msgRate = msgRateList[0]
                if payloadSizeindex == len(payloadSizeList):
                    state = 6
            else:
                msgRate += msgRateStep
            payloadSize = payloadSizeList[payloadSizeindex]
            # time.sleep(5)
            (result,mid)    = client.publish('/SUB/set/'+str(payloadSize)+'/'+str(float(msgRate/(activePub*1.0)))+'/'+str(float((msgTotal/float(10))/activePub)),"",qos=qos)
            state = 3
        elif state == 3:
            if readyPub == activePub:
                time.sleep(5)
                print "ready"
                ser.write('r')
                readyPub = 0
                state = 0
                continue
            # if time.time() - lastMsgTime > 10:
                # (result,mid)    = client.publish('/SUB/set/'+str(payloadSize)+'/'+str(float(msgRate/(activePub*1.0)))+'/'+str(float((msgTotal/float(10))/activePub)),"",qos=qos)
                # lastMsgTime = time.time()
        elif state == 4:
            while  time.time() - lastMsgTime < timeOut:
                y = ser.readline()
                # print y
                if y is None or len(y) < 0:
                   continue
                # print y
                datas = y.split(",")
                # print len(datas)
                currentList.append(float(datas[0]))
                voltageList.append(float(datas[1])/1000)
                powerList.append(float(datas[0])*(float(datas[1])/1000))
                checkcount = 0
                for i in range(activePub):
                    checkcount += sum(msgCountList[i])
                if checkcount > 0:
                    pass
                else:
                    state = 5
                    break
            # state = 6
        elif state == 5:
            # save file
            saveLatencyFile()
            savePowerConsumtion()
            saveResultFile()
            ser.write('f')
            print "save"
            state = 0
        elif state == 6:
            print "done"
            ser.write('d')
            break
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    client.loop_stop()
    client.disconnect()
    sys.exit(0)
