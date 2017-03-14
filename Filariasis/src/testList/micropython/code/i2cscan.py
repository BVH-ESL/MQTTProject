import machine, time
i2c = machine.I2C(machine.Pin(5), machine.Pin(4))

    print(i2c.scan())
    time.sleep(1)
