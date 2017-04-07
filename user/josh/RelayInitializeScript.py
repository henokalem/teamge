import RPi.GPIO as GPIO
import time

pins = [21,20,7,5,16,12,26,19,13,6]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in pins:   
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.3)
