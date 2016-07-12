import sys, time
import numpy as np
from matplotlib import pyplot as plt
from serial import Serial
from serial import SerialException

## specify your serial port here !!!
com_port = '/dev/ttyUSB0'
    # for Ubuntu: use '/dev/ttyUSB0' or '/dev/ttyACM0'

## specify baudrate !!!!
baudrate = 921600

timeout  = 1.0 # set serial I/O timeout in seconds

try:
    ser = Serial( port=com_port, baudrate=baudrate, timeout=timeout,
                  bytesize=8, parity='N', stopbits=1 )
except SerialException as ex:
    print ex
    sys.exit(-1)

nsteps = 3500
ymax = 3000     # 35 Celsius
ymin = 2000     # 20 Celsius
xdata = []
ydata = []

# fig = plt.figure()
fig, ax = plt.subplots()
data, = ax.plot( xdata, ydata )
plt.axis( [0,nsteps,ymin,ymax] )
plt.ion() # enable interactive plotting mode
plt.title('Power Consumtion')
plt.xlabel('')
plt.ylabel('mW')
plt.grid(True)
plt.show(block=False)

x = 0
new_y = []
value_text = None
value_min = 100
value_max = 0

try:
    while True:
        y = ser.readline()
        # print y
        if y is None or len(y) == 0:
           continue

        datas = (y.split(","))
        current = float(datas[0])
        voltage = float(datas[1])
        power = current*voltage/1000
        new_y.append( power )
        if len(new_y) < 10:
           continue
        for y in new_y:
            ydata.append(power)
            xdata.append(x)
            x += 1
        new_y = []

        if len(xdata) > nsteps:
            n = len(xdata)-nsteps
            del xdata[0:n]
            del ydata[0:n]
            plt.xlim( [x-nsteps+1,x] )
        else:
            plt.xlim( [0,nsteps] )
        data.set_data( xdata, ydata )

        #fig.canvas.draw()
        fig.canvas.flush_events()

except KeyboardInterrupt as ex:
    print 'Exit'
except Exception as ex:
    print 'Exception:', ex
finally:
    print 'Done...'
    pass
sys.exit(0)
