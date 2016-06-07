import os, sys, time, psutil
import argparse

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

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
        p = psutil.Process(pid)
        print (time.strftime("%H:%M:%S"))+", ",
        print str(p.cpu_percent(interval=1.0))+", ",
        print CPU_temp+", ",
        print str(p.memory_percent())+", ",
        print " "
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    # client.loop_stop()
    # client.disconnect()
    sys.exit(0)
