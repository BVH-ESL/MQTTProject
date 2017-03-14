from machine import Pin, SPI
import time
import ubinascii
hspi = SPI(1, baudrate=1000000, polarity=0, phase=0)
# hspi.init()
while 1:
    hspi.write(b'\x05')     # write 5 bytes on MOSI
    time.sleep(1)
