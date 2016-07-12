import os, sys, time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-pid", "--pid", required = True, help = "pid")
args = vars(ap.parse_args())

pid = str(args["pid"])

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
    p = os.popen('cat /proc/'+pid+'/stat')
    line = p.readline()
    proc = line.split()
    return (int(proc[13])+int(proc[14])+int(proc[15])+int(proc[16]))
    # return (proc)
    # i = 0
    # while 1:
    #     i = i + 1
    #     line = p.readline()
    #     if i==2:
    #        return(line.split()[1:4])
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

proctotal   = getProcTime(pid)
cputotal    = getCpuTime()

try:
    while 1:
        # print("start")
        pr_proctotal = proctotal
        pr_cputotal = cputotal

        proctotal = getProcTime(pid)
        cputotal = getCpuTime()
        res = ((proctotal - pr_proctotal) / (cputotal - pr_cputotal) * 100)
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]),1)
        RAM_used = round(int(RAM_stats[1]),1)
        RAM_free = round(int(RAM_stats[2]),1)
        print (time.strftime("%H:%M:%S"))+", ",
        print str(res)+", ",
        print str(RAM_total)+", ",
        print str(RAM_used)+", ",
        print str(RAM_free)+", ",
        print " "
        time.sleep(0.5)
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    # client.loop_stop()
    # client.disconnect()
    sys.exit(0)
