import argparse
import sys, os, time, datetime
import numpy as np
from matplotlib import pyplot as plt
import fnmatch

ap = argparse.ArgumentParser()
ap.add_argument(
    "-P", "--path", default="result",
    help="RPi Id for publish")
# ap.add_argument(
#     "-H", "--host", default="10.42.0.27",
#     help="MQTT host to connect to")
# ap.add_argument(
#     "-Q", "--qos", type=int, default=1,
#     help="QoS Level")
args = vars(ap.parse_args())

payloadLength   = 7
payloadList     = []
payloadCount    = -1
connrateList    = []
totalmsgList    = [ [] for x in range(payloadLength) ]
totaltimeList   = [ [] for x in range(payloadLength) ]
thoughputList   = [ [] for x in range(payloadLength) ]
avglatencyList  = [ [] for x in range(payloadLength) ]
avgpowerList    = [ [] for x in range(payloadLength) ]
avgvoltageList  = [ [] for x in range(payloadLength) ]
avgcurrentList  = [ [] for x in range(payloadLength) ]

path = args["path"]
for file in os.listdir(path):
    if fnmatch.fnmatch(file, 'over*.txt'):
        f = open(path + file, "r")
        # print file
        for line in f:
            payload     = line.split(',')[0]
            connrate    = line.split(',')[1]
            totalmsg    = line.split(',')[2]
            totaltime   = line.split(',')[3]
            thoughput   = line.split(',')[4]
            avglatency  = line.split(',')[5]
            avgpower    = line.split(',')[6]
            avgvoltage  = line.split(',')[7]
            avgcurrent  = line.split(',')[8]
            if payload in payloadList:
                if connrate in connrateList:
                    pass
                else:
                    connrateList.append(connrate)
                totalmsgList[payloadCount].append(totalmsg)
                totaltimeList[payloadCount].append(totaltime)
                thoughputList[payloadCount].append(thoughput)
                avglatencyList[payloadCount].append(avglatency)
                avgpowerList[payloadCount].append(avgpower)
                avgvoltageList[payloadCount].append(avgvoltage)
                avgcurrentList[payloadCount].append(avgcurrent.split('\n')[0])
            else:
                payloadList.append(payload)
                payloadCount+=1

# Plot things...
fig = plt.figure()

ax_power = plt.subplot(311)
for i in range(len(avgpowerList)):
    ax_power.plot(connrateList, avgpowerList[i], label=payloadList[i]+"Byte")
ax_power.legend(fancybox=True, title="Payload Size", loc='upper left')
# ax_thoughput.axis([connrateList[0],connrateList[len(connrateList)-1], minThoughput, maxThoughput])
ax_power.set_title('Power')
ax_power.set_xlabel('')
ax_power.set_ylabel('mW')
ax_power.grid(True)

ax_current = plt.subplot(312)
for i in range(len(avgcurrentList)):
    ax_current.plot(connrateList, avgcurrentList[i], label=payloadList[i]+"Byte")
# ax_current.legend(fancybox=True, title="Payload Size", loc='upper left')
# ax_thoughput.axis([connrateList[0],connrateList[len(connrateList)-1], minThoughput, maxThoughput])
ax_current.set_title('Current')
ax_current.set_xlabel('')
ax_current.set_ylabel('mA')
ax_current.grid(True)

ax_voltage = plt.subplot(313)
for i in range(len(avgvoltageList)):
    ax_voltage.plot(connrateList, avgvoltageList[i], label=payloadList[i]+"Byte")
# ax_voltage.legend(fancybox=True, title="Payload Size", loc='upper left')
# ax_thoughput.axis([connrateList[0],connrateList[len(connrateList)-1], minThoughput, maxThoughput])
ax_voltage.set_title('Voltage')
ax_voltage.set_xlabel('')
ax_voltage.set_ylabel('mV')
ax_voltage.grid(True)

plt.show()
