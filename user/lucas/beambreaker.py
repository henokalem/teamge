import RPi.GPIO as GPIO, time
import datetime

pin = 5

def beamBroken(channel):
    print("Broke {}".format(channel))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pin, GPIO.FALLING, callback=beamBroken, bouncetime=200)

while True:
    time.sleep(0.1)
