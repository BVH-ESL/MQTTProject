import time, math, machine

led = machine.PWM(machine.Pin(0), freq=1000)

def pulse(l, t):
    for i in range(20):
        l.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        time.sleep_ms(t)

while 1:
    pulse(led, 50)
