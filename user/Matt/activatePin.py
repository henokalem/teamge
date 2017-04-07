import time
import RPi.GPIO as GPIO, time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pin = int(sys.argv[1])

GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, GPIO.HIGH)
time.sleep(0.3)
GPIO.output(pin, GPIO.LOW)
