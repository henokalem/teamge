import lightHandler
import sys
import os
import time

light = lightHandler.lightHandler()

for i in range(100):
	light.setGreen()
	os.system("sudo python /home/pi/teamge/user/Matt/activatePin.py 13")
	time.sleep(2)
	light.setYellow()
	os.system("sudo python /home/pi/teamge/user/Matt/activatePin.py 6")
	time.sleep(2)
	light.setRed()
	os.system("sudo python /home/pi/teamge/user/Matt/activatePin.py 13")
	time.sleep(2)
	#light.setWhite()
	#os.system("sudo python /home/pi/teamge/user/Matt/activatePin.py 6")
	#time.sleep(1)	
