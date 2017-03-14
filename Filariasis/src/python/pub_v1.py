import machine
from method import METHOD

def main():
    connWIFI = METHOD()
    btn = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
    led = machine.Pin(2, machine.Pin.OUT) #D4
    led.value(not(led.value()))
    # while True:
    if btn.value():
        connWIFI.activateDeepSleep(1, 2000)

if __name__ == '__main__':
    main()
