import RPi.GPIO as GPIO
import time, datetime

mode = GPIO.getmode()
# print mode
GPIO.setmode(GPIO.BCM)
butPin = 17
GPIO.setup(butPin, GPIO.IN)
lastState = 1

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        if GPIO.input(butPin) == 0 and lastState == 1:
            print "press"
            time.sleep(0.001)
        elif GPIO.input(butPin) == 1 and lastState == 0:
            print "released"
            # print datetime.time(datetime.datetime.now())
            time.sleep(0.001)
        lastState = GPIO.input(butPin)
        # if (currentState == HIGH && lastState == LOW){//if button has just been pressed
        # Serial.println("pressed");
        # delay(1);//crude form of button debouncing
        # } else if(currentState == LOW && lastState == HIGH){
        # Serial.println("released");
        # delay(1);//crude form of button debouncing
        # }
        # print(GPIO.input(butPin))
        # # time.sleep(0.1)
        # # if GPIO.input(butPin): # button is released
        # #     pass
        # # else:
        # #     print("push")
except KeyboardInterrupt as ex:
    print 'Terminated...'
