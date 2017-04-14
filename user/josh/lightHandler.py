import string
import sys
import os
import time
import datetime
import GELight

GREEN = 0
YELLOW = 1
RED = 2
TIME_BUFFER = 1.0

class lightHandler:
    def __init__(self):
        self.color = GREEN
	self.light = GELight.GELight()
	self.light.setGreen()
        #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
        self.timeOfLastUpdate = datetime.datetime.utcnow()

    def setGreen(self):
        currentTime = datetime.datetime.utcnow()
        print("currentTime for light change: " + str(currentTime))
	print("total seconds from last light change: " + str((currentTime - self.timeOfLastUpdate).total_seconds()))
        
	if self.color != GREEN:
	    if(currentTime - self.timeOfLastUpdate).total_seconds() > TIME_BUFFER:
                self.color = GREEN
                print("Setting light to -------------------------------------------------------------- green")
                #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
		self.light.setOff()
                self.light.setGreen()
		self.light.setGreen()
		self.timeOfLastUpdate = datetime.datetime.utcnow()
            else:
		print("----------------------------------------------------------------- must wait to change light to green!")

        else:
            print("------------------------------------------------------Light is already green!")
            

    def setYellow(self):
        currentTime = datetime.datetime.utcnow()
        print("currentTime for light change: " + str(currentTime))
	print("total seconds from last light change: " + str((currentTime - self.timeOfLastUpdate).total_seconds()))
        
	if self.color != YELLOW:
            if(currentTime - self.timeOfLastUpdate).total_seconds() > TIME_BUFFER:
                self.color = YELLOW
                print("Setting light to -------------------------------------------------------------- yellow")
                self.light.setOff()
		self.light.setYellow()
		#os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py")
                self.timeOfLastUpdate = datetime.datetime.utcnow()
            else:
		print("----------------------------------------------------------------- must wait to change light to yellow!")
            

        else:
            print("------------------------------------------------------Light is already Yellow!")


    def setRed(self):
        currentTime = datetime.datetime.utcnow()
        print("currentTime for light change: " + str(currentTime))
	print("total seconds from last light change: " + str((currentTime - self.timeOfLastUpdate).total_seconds()))
        
	if self.color != RED:
            if(currentTime - self.timeOfLastUpdate).total_seconds() > TIME_BUFFER:
                self.color = RED
                print("Setting light to -------------------------------------------------------------- red")
                self.light.setOff()
		self.light.setRed()
		#os.system("sudo python /home/pi/teamge/user/Matt/setRed.py")
                self.timeOfLastUpdate = datetime.datetime.utcnow()
            else:
		print("----------------------------------------------------------------- must wait to change light to red!")
            

        else:
            print("------------------------------------------------------Light is already Red!")
            
