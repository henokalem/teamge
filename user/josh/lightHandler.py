import string
import sys
import os
import time
import datetime

GREEN = 0
YELLOW = 1
RED = 2

class lightHandler:
    def __init__(self):
        self.color = GREEN
        os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
        self.timeOfLastUpdate = datetime.datetime.utcnow()

    def setGreen(self):
        currentTime = datetime.datetime.utcnow()
        
        if self.color != GREEN and (currentTime - self.timeOfLastUpdate).total_seconds > 1.0:
            self.color = GREEN
            os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
            self.timeOfLastUpdate = datetime.datetime.utcnow()
            

        else:
            print("------------------------------------------------------Light is already green!")
            

    def setYellow(self):
        currentTime = datetime.datetime.utcnow()
        
        if self.color != YELLOW and (currentTime - self.timeOfLastUpdate).total_seconds > 1.0:
            self.color = YELLOW
            os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py")
            self.timeOfLastUpdate = datetime.datetime.utcnow()
            

        else:
            print("------------------------------------------------------Light is already Yellow!")


    def setRed(self):
        currentTime = datetime.datetime.utcnow()
        
        if self.color != RED and (currentTime - self.timeOfLastUpdate).total_seconds > 1.0:
            self.color = RED
            os.system("sudo python /home/pi/teamge/user/Matt/setRed.py")
            self.timeOfLastUpdate = datetime.datetime.utcnow()
            

        else:
            print("------------------------------------------------------Light is already Red!")
            
