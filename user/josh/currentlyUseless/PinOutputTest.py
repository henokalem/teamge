##from Turnout import Turnout
##import time
##
##test=Turnout(1,21,20)
##time.sleep(1)
##test.activateTurn()
##time.sleep(1)
##
##test=Turnout(2,7,5)
##time.sleep(1)
##test.activateTurn()
##time.sleep(1)
##
##test=Turnout(3,16,12)
##time.sleep(1)
##test.activateTurn()
##time.sleep(1)
##
##test=Turnout(4,26,19)
##time.sleep(1)
##test.activateTurn()
##time.sleep(1)
##
##test=Turnout(5,13,6)
##time.sleep(1)
##test.activateTurn()
##time.sleep(1)

import RPi.GPIO as GPIO
import time

pin_num = int(input("Enter a pin number to test: "))
while True:
    #
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_num, GPIO.OUT)

    time.sleep(1)
    GPIO.output(pin_num, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(pin_num, GPIO.LOW)
    pin_num = int(input("Enter a pin number to test: "))
