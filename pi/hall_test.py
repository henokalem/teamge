import RPi.GPIO as g
# import time for sleeping and sys for exit command
import time
import sys

g.setmode(g.BCM)
g.setup(4, g.IN)

sensor = 1 
while (1):
	time.sleep(0.5)
	sensor = g.input(4)
	print("sensor is {}".format(sensor))
