import os, sys

pGet = os.popen('ps aux | grep mosquitto')
line = pGet.readline()
print ( line.split())
pid = line.split()[1]
print "before kill" + pid
pKill = os.popen('kill -KILL '+pid)
pOpen = os.popen('mosquitto -d')
pGet = os.popen('ps aux | grep mosquitto')
line = pGet.readline()
print ( line.split())
pid = line.split()[1]
print "after kill" + pid
