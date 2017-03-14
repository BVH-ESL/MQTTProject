from machine import Pin

def callback(p):
    mypin.value(mypin.value() ^ 1)

btn = Pin(5, Pin.IN, Pin.PULL_UP)
mypin = Pin(4, Pin.OUT)

btn.irq(trigger=Pin.IRQ_FALLING, handler=callback)

while 1:
    pass
