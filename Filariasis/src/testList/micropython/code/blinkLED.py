import machine, time

led = machine.Pin(2, machine.Pin.OUT) #D1

while 1:
    print("ei")
    led.high()
    time.sleep(0.5)
    led.low()
    time.sleep(0.5)
