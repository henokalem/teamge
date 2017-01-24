import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# init list with pin numbers 

pinList = [26, 19, 13, 6, 5, 21, 20, 16, 17, 25]

# loop through pins and set mode and state to 'low'

for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)

# time to sleep between operations in the main loop

SleepTimeL = 0.5

# main loop

try: 
	while True:

		for i in pinList:
			GPIO.output(i, GPIO.HIGH)
			time.sleep(SleepTimeL)
			GPIO.output(i, GPIO.LOW)

		pinList.reverse()

		for i in pinList:
			GPIO.output(i, GPIO.HIGH)
			time.sleep(SleepTimeL)
			GPIO.output(i, GPIO.LOW)

		pinList.reverse()

# End program cleanly with keyboard
except KeyboardInterrupt:
	print " Quit"

	# Reset GPIO settings
	GPIO.cleanup()
