import os, sys, time, psutil
import argparse

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

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

try:
    while 1:
        CPU_temp = getCPUtemperature()
        # print "cpu temp : " + CPU_temp
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]),1)
        RAM_used = round(int(RAM_stats[1]),1)
        RAM_free = round(int(RAM_stats[2]),1)
        # print "ram total : " + str(RAM_total)
        # print "ram used : " + str(RAM_used)
        # print "ram free : " + str(RAM_free)
        p = psutil.Process(pid)
        print (time.strftime("%H:%M:%S"))+", ",
        print str(p.cpu_percent(interval=1.0))+", ",
        print CPU_temp+", ",
        print str(RAM_total)+", ",
        print str(RAM_used)+", ",
        print str(RAM_free)+", ",
        print " "
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    # client.loop_stop()
    # client.disconnect()
    sys.exit(0)
