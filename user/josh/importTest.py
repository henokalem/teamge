import sys

import os
path="/home/pi/Desktop/JMRI/lib"  # insert the path to the directory of interest here
dirList=os.listdir(path)
for fname in dirList:
    #print fname
    if(".jar" in fname):
        sys.path.append("/home/pi/Desktop/JMRI/lib/"+fname)

sys.path.append("/home/pi/Desktop/JMRI/jmri.jar")
sys.path.append("/home/pi/Desktop/JMRI/jmriplugins.jar")

sys.path.append("/home/pi/Desktop/apache-log4j-1.2.17/log4j-1.2.17.jar")
sys.path.append("/home/pi/Desktop/slf4j-1.7.23/slf4j-api-1.7.23.jar")
sys.path.append("/home/pi/Desktop/slf4j-1.7.23/slf4j-simple-1.7.23.jar")
sys.path.append("/home/pi/Desktop/jdom-2.0.6/jdom-2.0.6-contrib.jar")
sys.path.append("/home/pi/Desktop/jdom-2.0.6/jdom-2.0.6-javadoc.jar")
sys.path.append("/home/pi/Desktop/jdom-2.0.6/jdom-2.0.6-junit.jar")
sys.path.append("/home/pi/Desktop/jdom-2.0.6/jdom-2.0.6-sources.jar")
sys.path.append("/home/pi/Desktop/xerceslmpl-2.9.0.jar")


import org.apache.log4j
import org.jdom2
import jmri
import jarray


import java.io

org.apache.log4j.PropertyConfigurator.configure("/home/pi/Desktop/JMRI/default.lcf")

fileLocation = "My_JMRI_Railroad/profile/profile.properties"
#configFileLocation = jmri.util.FileUtil.getPreferencesPath()+fileLocation
configFileLocation = "/home/pi/.jmri/" + fileLocation
print("File location: " + configFileLocation)
configfile = java.io.File(configFileLocation)
jmri.InstanceManager.setConfigureManager(jmri.configurexml.ConfigXmlManager())
jmri.InstanceManager.getDefault(jmri.ConfigureManager).load(configfile)

print "Hello world!"

class BackAndForthTimed(jmri.jmrit.automat.AbstractAutomaton) :

        def init(self):
                # init() is called exactly once at the beginning to do
                # any necessary configuration.
                print "Inside init(self)"
                

                # get loco address. For long address change "False" to "True"
                
                self.throttle = self.getThrottle(1, False)  # short address 14

                return

        def handle(self):
                # handle() is called repeatedly until it returns false.
                print "Inside handle(self)"

                # Turn power on
                print "Turning power on" 
                LayoutPowerOn().start()

                # set loco to forward
                #print "Set Loco Forward"
                #self.throttle.setIsForward(True)
                
                # wait 1 second for engine to be stopped, then set speed
                #self.waitMsec(1000)                 
                #print "Set Speed"
                #self.throttle.setSpeedSetting(0.7)

                # wait for run time in forward direction
                #print "Wait for forward time"
                #self.waitMsec(10000)
                
                # stop the engine
                #print "Set Speed Stop"
                #self.throttle.setSpeedSetting(0)

                # delay for a time (remember loco could still be moving
                # due to simulated or actual inertia). 
                print "wait 3 seconds"
                self.waitMsec(3000) 
                
                # set direction to reverse, set speed
                #print "Set Loco Reverse"
                #self.throttle.setIsForward(False)
                #self.waitMsec(1000)                 # wait 1 second for Xpressnet to catch up
                #print "Set Speed"
                #self.throttle.setSpeedSetting(0.7)

                # wait for run time in reverse direction
                #print "Wait for reverse time"
                #self.waitMsec(10000)
                #print "Set Speed Stop"
                #self.throttle.setSpeedSetting(0)
                
                # delay for a time (remember loco could still be moving
                # due to simulated or actual inertia). Time is in milliseconds
                #print "wait 3 seconds"
                #self.waitMsec(3000)
        
                # Shut layout power off
                print "Turning power off"
                LayoutPowerOff().start()
                
                # and continue around again
                print "End of Loop"
                return 0        
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
            #jmri.InstanceManager.powerManagerInstance()
                powermanager.setPower(jmri.PowerManager.OFF)
                return 0

# End of power classes

# start one of these up
a = BackAndForthTimed()
a.start()
