import machine, time

# D1
btn = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
# D2
led = machine.Pin(4, machine.Pin.OUT)

while 1:
    if btn.value():
        led.low()
    else:
        led.high()
    # print btn.value()
    # if btn.value():
        # print "You push Button"
