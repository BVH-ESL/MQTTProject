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
y_power_max = 3000
y_power_min = 1500
xdata = []
ydata_power = []

fig = plt.figure()
# plt.subplots(311)
ax_power = fig.add_subplot(311)
data_power, = ax_power.plot( xdata, ydata_power )
ax_power.axis( [0, nsteps, y_power_min, y_power_max] )
ax_power.axes.get_xaxis().set_visible(False)
# ax_power.ion() # enable interactive plotting mode
ax_power.set_title('Power Consumtion')
ax_power.set_xlabel('')
ax_power.set_ylabel('mW')
ax_power.grid(True)
# ax_power.show(block=False)

y_current_max = 500
y_current_min = 250
ydata_current = []

ax_current = fig.add_subplot(312)
data_current, = ax_current.plot( xdata, ydata_current )
ax_current.axis( [0, nsteps, y_current_min, y_current_max] )
ax_current.axes.get_xaxis().set_visible(False)
# plt.ion() # enable interactive plotting mode
ax_current.set_title('Current')
ax_current.set_xlabel('')
ax_current.set_ylabel('mA')
ax_current.grid(True)
# ax_current.show(block=False)

y_voltage_max = 5.5
y_voltage_min = 4.4
ydata_vloatge = []

ax_voltage = fig.add_subplot(313)
data_voltage, = ax_voltage.plot( xdata, ydata_vloatge )
ax_voltage.axis( [0, nsteps, y_voltage_min, y_voltage_max] )
# ax_voltage.ion() # enable interactive plotting mode
ax_voltage.set_title('Voltage')
ax_voltage.set_xlabel('')
ax_voltage.set_ylabel('mV')
ax_voltage.grid(True)
# ax_voltage.show(block=False)
plt.ion()
plt.show()

x = 0
new_y = []
value_text = None
value_min = 100
value_max = 0
try:
    while True:
        y = ser.readline()
        # print y
        if y is None or len(y) == 0 or y == "s":
           continue

        datas = (y.split(","))
        current = float(datas[0])
        voltage = float(datas[1])/1000
        power = current*voltage
        new_y.append( power )

        if len(new_y) < 10:
           continue
        for y in new_y:
            ydata_power.append(power)
            ydata_current.append(current)
            ydata_vloatge.append(voltage)
            xdata.append(x)
            x += 1
        new_y = []

        if len(xdata) > nsteps:
            n = len(xdata)-nsteps
            del xdata[0:n]
            del ydata_power[0:n]
            del ydata_current[0:n]
            del ydata_vloatge[0:n]
            plt.xlim( [x-nsteps+1,x] )
        else:
            plt.xlim( [0,nsteps] )

        data_power.set_data( xdata, ydata_power )
        data_current.set_data( xdata, ydata_current )
        data_voltage.set_data( xdata, ydata_vloatge )

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
