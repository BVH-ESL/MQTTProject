import os, sys

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

try:
    while 1:
        # CPU informatiom
        CPU_temp = getCPUtemperature()
        CPU_usage = getCPUuse()
        print "cpu temp : " + CPU_temp
        print "cpu usage : " + CPU_usage
        # RAM information
        # Output is in kb, here I convert it in Mb for readability
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000,1)
        RAM_used = round(int(RAM_stats[1]) / 1000,1)
        RAM_free = round(int(RAM_stats[2]) / 1000,1)
        print "ram total : " + str(RAM_total)
        print "ram used : " + str(RAM_used)
        print "ram free : " + str(RAM_free)
        # Disk information
        # DISK_stats = getDiskSpace()
        # DISK_total = DISK_stats[0]
        # DISK_free = DISK_stats[1]
        # DISK_perc = DISK_stats[3]
        print " "
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    # client.loop_stop()
    # client.disconnect()
    sys.exit(0)
