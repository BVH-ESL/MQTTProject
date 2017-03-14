import sys, os, time, datetime, csv, json, argparse
from serial import Serial
from serial import SerialException

# init variable for serial communication
com_port = '/dev/ttyUSB0'       # setting port for serial
baudrate = 921600               # setting baudrate for Serial
timeout = 1.0                   # setting timeout for serial

# directory variable for keep result of testing
# brokerType      = args["broker"]
directory      = "result"

# check directory is had
if not os.path.exists(directory):
    os.makedirs(directory)

# make connection with NodeMCU via serial
try:
    ser = Serial( port=com_port, baudrate=baudrate, timeout=timeout,
                  bytesize=8, parity='N', stopbits=1 )
except SerialException as ex:
    print ex
    sys.exit(-1)

txtFileName = directory+"/result_WAKE_RF_DEFAULT2.txt"
file = open(txtFileName, "w")
try:
    while 1:
        y = ser.readline()
        if y is None or len(y) == 0:
            continue
        else:
            file.write(y)
            # print y
except KeyboardInterrupt as ex:
    print 'Terminated...'
finally:
    file.close()
    sys.exit(0)
