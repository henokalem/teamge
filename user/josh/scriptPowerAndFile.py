# This is an example script for a JMRI "Automat" in Python
# It is based on the AutomatonExample.
#
# It runs a locomotive back and forth using time delays. 
#
# Times are in milliseconds
#
# Author: Bob Jacobsen, July 2008
# Based on BackAndForth.py 
# Author: Howard Watkins, January 2007
# Part of the JMRI distribution

import jmri
import jarray
import csv

class Train(object):
    def __init__(self, decoderID, speed, isForward):
        self.decoderID = decoderID
        self.speed = speed
        self.isForward = isForward


class TrainHandler(jmri.jmrit.automat.AbstractAutomaton) :

        def init(self):
                # init() is called exactly once at the beginning to do
                # any necessary configuration.
                print "Inside init(self)"

                self.continueLoop = False
                self.trains = []
                self.initialized = False

                print "reading from file"
                try:
                    f = open('/home/pi/teamge/user/josh/trainProperties.txt')
                    try:
                        reader = csv.reader(f)
                        firstRow = True
                        for row in reader:
                            if(firstRow):
                                print "Reading from first row"
                                if(row[0] == "True"):
                                    self.continueLoop = True
                                elif(row[0] == "False"):
                                    self.continueLoop = False
                                else:
                                    print("error")
                                firstRow = False
                            else:
                                print "Reading from another row"
                                print(str(row[0])+","+str(row[1])+str(row[2]))
                                newTrain = Train(int(row[0]),float(row[1]),bool(row[2]=="True"))
                                self.trains.append(newTrain)
                    finally:
                        f.close()
                except IOError:
                    print("Could not open file")

                print "Throttle"
                self.throttle = self.getThrottle(3, False)
                print "After throttle"

                print "Throttle 2"
                self.throttle1 = self.getThrottle(1, False)
                print "after throttle 2"

                return

        def handle(self):
                # handle() is called repeatedly until it returns false.
                #print "Inside handle(self)"

                if(self.initialized == False):
                    LayoutPowerOn().start()
                    self.throttle.setSpeedSetting(self.trains[0].speed)
                    self.throttle.setIsForward(self.trains[0].isForward)
                    self.throttle1.setSpeedSetting(self.trains[1].speed)
                    self.throttle1.setIsForward(self.trains[1].isForward)
                    self.initialized = True


                self.waitMsec(500)
                #print "reading from file"
                try:
                    f = open('/home/pi/teamge/user/josh/trainProperties.txt')
                    try:
                        reader = csv.reader(f)
                        firstRow = True
                        currentRow = 0
                        for row in reader:
                            if(firstRow):
                                #print "Reading from first row"
                                if(row[0] == "True"):
                                    self.continueLoop = True
                                elif(row[0] == "False"):
                                    self.continueLoop = False
                                else:
                                    print("error")
                                firstRow = False
                            else:
                                #print "Reading from another row"
                                #print self.trains[currentRow].decoderID
                                #print int(row[0])
                                #print currentRow
                                if(self.trains[currentRow].decoderID != int(row[0])):
                                    print "File decoder ID does not match train ID"
                                if(self.trains[currentRow].speed != float(row[1])):
                                    print "Changing speed for train: " + str(currentRow)
                                    self.trains[currentRow].speed = float(row[1])
                                    if currentRow == 0:
                                        #First train
                                        self.throttle.setSpeedSetting(self.trains[currentRow].speed)
                                    elif currentRow == 1:
                                        #Second Train
                                        self.throttle1.setSpeedSetting(self.trains[currentRow].speed)
                                if(self.trains[currentRow].isForward != bool(row[2]=="True")):
                                    print "Changing direction for train: " + str(currentRow)
                                    self.trains[currentRow].isForward = bool(row[2]=="True")
                                    if currentRow == 0:
                                        #First train
                                        self.throttle.setIsForward(self.trains[currentRow].isForward)
                                    elif currentRow == 1:
                                        #Second Train
                                        self.throttle1.setIsForward(self.trains[currentRow].isForward)
                                currentRow = currentRow + 1
                                #newTrain = Train(int(row[0]),float(row[1]),bool(row[2]))
                                #self.trains.append(newTrain)
                    finally:
                        f.close()
                except IOError:
                    print("Could not open file")
        
                # Shut layout power off
                if(not self.continueLoop):
                    self.throttle.setSpeedSetting(self.trains[0].speed)
                    self.throttle1.setSpeedSetting(self.trains[1].speed)
                    self.waitMsec(1000)
                    print "Turning power off"
                    LayoutPowerOff().start()
                
                # and continue around again if continue loop is true
                #print "End of Loop"
                return int(self.continueLoop)    
                # (requires JMRI to be terminated to stop - caution
                # doing so could leave loco running if not careful)

# end of class definition

# Start of power classes

class LayoutPowerOn(jmri.jmrit.automat.AbstractAutomaton):
        def init(self):
                self.condition = 'on' 
 
        def handle(self):
                powermanager.setPower(jmri.PowerManager.ON)
                return 0

class LayoutPowerOff(jmri.jmrit.automat.AbstractAutomaton):
        def init(self):
                self.condition = 'off'

        def handle(self):
                powermanager.setPower(jmri.PowerManager.OFF)
                return 0

# End of power classes

# start one of these up
TrainHandler().start()
