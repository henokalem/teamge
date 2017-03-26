import RPi.GPIO as GPIO
import time

pin_num = int(input("Enter a pin number to test: "))
while True:
    #
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.output(pin_num, GPIO.LOW)

    time.sleep(1)
    GPIO.output(pin_num, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(pin_num, GPIO.LOW)
    pin_num = int(input("Enter a pin number to test: "))

