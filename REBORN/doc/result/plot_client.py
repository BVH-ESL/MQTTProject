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

payloadLength   = 4
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

# path = args["path"]
path = "resultRPiQoS0(1)/"
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

maxThoughput = 0
minThoughput = 0
maxTime      = 0
minTime      = 0
print len(thoughputList[0])
print len(connrateList)
# Plot things...
fig = plt.figure()
ax_thoughput = plt.subplot(211)
for i in range(len(thoughputList)):
    # if max(thoughputList[i]) > maxThoughput:
    #     maxThoughput = max(thoughputList[i])
    # if min(thoughputList[i]) < minThoughput:
    #     minThoughput = min(thoughputList[i])
    ax_thoughput.plot(connrateList, thoughputList[i], label=payloadList[i]+"Byte")
# print maxThoughput
# print minThoughput
ax_thoughput.legend(fancybox=True, title="Payload Size", loc='upper left')
# ax_thoughput.axis([connrateList[0],connrateList[len(connrateList)-1], minThoughput, maxThoughput])
ax_thoughput.set_title('Thoughput')
ax_thoughput.set_xlabel('')
ax_thoughput.set_ylabel('MpS(Message per Second)')
ax_thoughput.grid(True)
# ax_thoughput.set_xlim([connrateList[0],connrateList[len(connrateList)-1]])

ax_latency = plt.subplot(212)
for i in range(len(totaltimeList)):
    # if max(totaltimeList[i]) > maxTime:
    #     maxTime = max(totaltimeList[i])
    # if min(totaltimeList[i]) < minTime:
    #     minTime = min(totaltimeList[i])
    ax_latency.plot(connrateList, totaltimeList[i], label=payloadList[i]+"Byte")
# ax_latency.axis([connrateList[0],connrateList[len(connrateList)-1], minTime, maxTime])
ax_latency.set_title('Total Time')
ax_latency.set_xlabel('')
ax_latency.set_ylabel('Second')
ax_latency.grid(True)

# plt.xlim([500, connrateList[len(connrateList)-1]])
plt.show()
# fig2 = plt.figure()
# plt.title('Latency')
# # plt.xlim([1000,13000])
# for i in range(len(thoughputList)):
#     plt.plot(connrateList, totaltimeList[i], label=payloadList[i]+"Byte")
# plt.legend(fancybox=True, title="Payload Size", loc='upper right')
# # plt.legend(connrateList, payloadList, loc='upper right', shadow=True)
# plt.show()
