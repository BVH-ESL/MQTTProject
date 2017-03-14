from machine import Pin, SPI
import time
import ubinascii

vref = 3.3
cs = Pin(15, Pin.OUT)
cs.high()
hspi = SPI(1, baudrate=1600000, polarity=0, phase=0)
value = bytearray(2)

while True:
    data = bytearray(2)
    wget = b'\xA0\x00'
    cs.low()
    hspi.write(b'\x01')
    hspi.write(b'\xA0')
    data = hspi.read(1)
    # data = hspi.write_readinto(wget, data)
    cs.high()
    print(str(int(ubinascii.hexlify(data & b'\x0fff'))*vref/4096))
    time.sleep(1)
    # data = data*vref/4096
    # time.sleep(1)
    # print(str(data & b'\x0fff'))
