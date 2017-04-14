import string
import sys
import os
import time
import datetime
import GELight

#constants for keeping track of the light and time buffer between light changes so it doesn't flash like crazy
GREEN = 0
YELLOW = 1
RED = 2
WHITE = 3
TIME_BUFFER = 1.0

class lightHandler:
    def __init__(self):
	#sets up the light and initializes to green
        self.color = GREEN
	self.light = GELight.GELight()
	self.light.setGreen()
        #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
        self.timeOfLastUpdate = datetime.datetime.utcnow()
	self.greenCounter = 0	
 
    def setGreen(self):
        currentTime = datetime.datetime.utcnow()
        print("currentTime for light change: " + str(currentTime))
	print("total seconds from last light change: " + str((currentTime - self.timeOfLastUpdate).total_seconds()))
	self.greenCounter = (self.greenCounter + 1) % 3

	if(self.greenCounter == 2):
		self.color = GREEN
		print("Setting light to -------------------------------------------------------------- green to help clear weird bug")
		self.light.setOff()
		self.light.setGreen()
		greenCounter = 0
		self.timeOfLastUpdate = datetime.datetime.utcnow()
		return

	if self.color != GREEN:
	    if(currentTime - self.timeOfLastUpdate).total_seconds() > TIME_BUFFER:
                self.color = GREEN
                #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
                print("Setting light to -------------------------------------------------------------- green")
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
 
    def setWhite(self):
        currentTime = datetime.datetime.utcnow()
        print("currentTime for light change: " + str(currentTime))
	print("total seconds from last light change: " + str((currentTime - self.timeOfLastUpdate).total_seconds()))
        
	if self.color != WHITE:
	    if(currentTime - self.timeOfLastUpdate).total_seconds() > TIME_BUFFER:
                self.color = WHITE
                print("Setting light to -------------------------------------------------------------- white")
                #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
		self.light.setOff()
                self.light.setWhite()
		self.timeOfLastUpdate = datetime.datetime.utcnow()
            else:
		print("----------------------------------------------------------------- must wait to change light to white!")

        else:
            print("------------------------------------------------------Light is already white!")
            
