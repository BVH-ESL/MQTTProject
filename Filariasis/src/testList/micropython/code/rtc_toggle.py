import machine

def toggle():
    led = machine.Pin(2, machine.Pin.OUT)
    led.value(led.value() ^ 1)
    print ("toggle")

# print ("start")
rtc = machine.RTC()

rtc.irq(trigger=rtc.ALARM0, handler=toggle())
rtc.alarm(rtc.ALARM0, 1000, repeat=True)
# D2

# set RTC.ALARM0 to fire after 10 seconds (waking the device)
