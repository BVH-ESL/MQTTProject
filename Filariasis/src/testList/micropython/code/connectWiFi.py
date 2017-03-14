import network, time

sta_if = network.WLAN(network.STA_IF)

while 1:
    sta_if.scan()
    time.sleep(5)
