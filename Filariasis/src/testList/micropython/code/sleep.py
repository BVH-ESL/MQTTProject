import machine, micropython

# configure RTC.ALARM0 to be able to wake the device
micropython.alloc_emergency_exception_buf(100)
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

# set RTC.ALARM0 to fire after 10 seconds (waking the device)
rtc.alarm(rtc.ALARM0, 5000)

# put the device to sleep
machine.deepsleep()
