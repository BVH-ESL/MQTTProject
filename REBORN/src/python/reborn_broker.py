import os, sys, time, datetime, csv
import argparse
# from pathlib import Path
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butPin = 21
GPIO.setup(butPin, GPIO.IN)
stpPin = 20
GPIO.setup(stpPin, GPIO.IN)
# finPin = 16
GPIO.setup(26, GPIO.OUT, initial=1)
GPIO.setwarnings(False)
state = 0

def getUptime():
    p = os.popen('cat /proc/uptime')
    line = p.readline()
    return ( line.split())

def getCpuTime():
    p = os.popen('cat /proc/stat')
    return sum(map(float, p.readline().split(' ')[2:]))

def getProcTime(pid):
    p = os.popen('cat /proc/'+str(pid)+'/stat')
    line = p.readline()
    proc = line.split()
    return (int(proc[13])+int(proc[14])+int(proc[15])+int(proc[16]))

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

def saveOverrall(now):
    global cpulist
    global ramuselist
    # now = datetime.datetime.now()
    txtFileName = "resultRPiQos1/overrall"+now.strftime('%m%d%Y-%H')+".txt"
    bufferString = now.strftime('%m/%d/%Y %H:%M:%S')+','+str(sum(cpulist)/len(cpulist))+', '+str(sum(ramuselist)/len(ramuselist))+'\n'
    file = open(txtFileName, 'a')
    file.write(bufferString)
    file.close()

def saveTrend(now):
    global cpulis
    global ramuselist
    # now = datetime.datetime.now()
    txtFileName = "resultRPiQos1/trend"+now.strftime('%m%d%Y-%H%M%S')+".txt"
    file = open(txtFileName, "w")
    for i in range(len(cpulist)):
        bufferString = str(cpulist[i])+','+str(ramuselist[i])+'\n'
        file.write(bufferString)
    file.close()

ap = argparse.ArgumentParser()
ap.add_argument("-pid", "--pid", required = True, help = "pid")
args = vars(ap.parse_args())
pid = int(args["pid"])

# proctotal   = getProcTime(pid)
# cputotal    = getCpuTime()
cpulist     = []
ramuselist  = []

try:
    while 1:
        if state == 0:
            if GPIO.input(butPin) == 1:
                GPIO.output(26, 1)
                print "start"
                state = 1
                proctotal   = getProcTime(pid)
                cputotal    = getCpuTime()

        elif state == 1:
            if GPIO.input(stpPin) == 0:
                state = 2
                print "done"
                continue

            pr_proctotal = proctotal
            pr_cputotal = cputotal

            proctotal = getProcTime(pid)
            cputotal = getCpuTime()
            res = ((proctotal - pr_proctotal) / (cputotal - pr_cputotal) * 100)

            RAM_stats = getRAMinfo()
            RAM_total = round(int(RAM_stats[0]),1)
            RAM_used = round(int(RAM_stats[1]),1)
            RAM_free = round(int(RAM_stats[2]),1)

            cpulist.append(res)
            ramuselist.append(RAM_used)
            time.sleep(0.02)
        elif state == 2:
            print "cpu avg, ram usage avg"
            print str(sum(cpulist)/len(cpulist))+','+str(sum(ramuselist)/len(ramuselist))
            # save file
            # save = datetime.datetime.now()
            saveTrend(datetime.datetime.now())
            saveOverrall(datetime.datetime.now())
            print "save Done"
            GPIO.output(26, 0)
            # time.sleep(0.2)
            state = 0
except KeyboardInterrupt as ex:
    # print "cpu avg, ram usage avg"
    # print str(sum(cpulist)/len(cpulist))+','+str(sum(ramuselist)/len(ramuselist))
    # print 'Terminated...'
    GPIO.cleanup()
finally:
    # client.loop_stop()
    # client.disconnect()
    GPIO.cleanup()
    sys.exit(0)
