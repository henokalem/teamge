import RPi.GPIO as GPIO, time
import datetime


GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
GPIO.setup(25, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(13, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(26, GPIO.IN)

print("start")
while True:
    # values = [GPIO.input(12), 
    #           GPIO.input(25), 
    #           GPIO.input(24), 
    #           GPIO.input(23), 
    #           GPIO.input(18), 
    #           GPIO.input(13), 
    #           GPIO.input(5), 
    #           GPIO.input(6), 
    #           GPIO.input(26)]

    time.sleep(1)
    print(GPIO.input(12))
