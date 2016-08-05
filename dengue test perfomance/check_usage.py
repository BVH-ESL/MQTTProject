import os, sys, time, psutil
import argparse
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
butPin = 21
GPIO.setup(butPin, GPIO.IN)
stpPin = 20
GPIO.setup(stpPin, GPIO.IN)
state = 1

def getUptime():
    # print "get up time"
    p = os.popen('cat /proc/uptime')
    line = p.readline()
    # uptime = line.split()
    # return (uptime[0])
    return ( line.split())

def getCpuTime():
    p = os.popen('cat /proc/stat')
    return sum(map(float, p.readline().split(' ')[2:]))

def getProcTime(pid):
    # print "dkdk"
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
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-pid", "--pid", required = True, help = "pid")
# ap.add_argument("-np", "--numpub", required = True, help = "numpub")
# ap.add_argument("-nt", "--numthred", required = True, help = "numthred")
args = vars(ap.parse_args())

pid = int(args["pid"])

proctotal   = getProcTime(pid)
cputotal    = getCpuTime()
cpulist     = []
ramuselist  = []

try:
    while 1:
        if state == 1:
            if GPIO.input(butPin) == 0:
                state = 2
        else:
            if GPIO.input(stpPin) == 0:
                print "cpu avg, ram usage avg"
                print str(sum(cpulist)/len(cpulist))+','+str(sum(ramuselist)/len(ramuselist))
                break
                # sys.exit(0)

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
            # print str(res)+", ",
            # print str(RAM_total)+", ",
            # print str(RAM_used)+", ",
            # print str(RAM_free)+", ",
            # print " "
            time.sleep(0.02)
except KeyboardInterrupt as ex:
    print "cpu avg, ram usage avg"
    print str(sum(cpulist)/len(cpulist))+','+str(sum(ramuselist)/len(ramuselist))
    print 'Terminated...'
finally:
    # client.loop_stop()
    # client.disconnect()
    sys.exit(0)
