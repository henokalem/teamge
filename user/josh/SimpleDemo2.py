import RPi.GPIO as GPIO, time
import datetime
import os

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        print("Time since last activation of " + str(channel) + ": " + str(datetime.datetime.utcnow()-self.time_of_last_break))
        if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time:
            #Call activated function
            self.beam_breaker_bank.activated(channel, self.pin_id, self.left_block, self.right_block)
        else:
            #Time was too short, was same train
            print("The same train activated the beam break!")
        self.time_of_last_break = datetime.datetime.utcnow()

    #Constructor
    # Left and righ blocks determined by Couner-clockwise orienation
    def __init__(self, pin_id, left_block, right_block, beam_breaker_bank):
        self.pin_id = pin_id
        self.left_block = left_block
        self.right_block = right_block
        self.beam_breaker_bank = beam_breaker_bank
    	self.wait_time = 1
    	self.time_of_last_break = datetime.datetime.utcnow()

        # Set up the initial GPIO pin ouputs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin_id, GPIO.FALLING, callback=self.beamBroken, bouncetime=200)

# Class for holding all of the beam breakers
class BeamBreakerBank:
    # Constructor
    def __init__(self):
    	self.beam_breaker = []
    	self.trains = []
	
    	# Set up beam breakers, change if you change the ports for
    	#  the beam breakers or add more (need to fix blocks).
    	#  Blocks determined by counter-clockwise orientation.
    	self.beam_breaker.append(BeamBreaker(16,1,2,self))
    	self.beam_breaker.append(BeamBreaker(6,1,2,self))
    	self.beam_breaker.append(BeamBreaker(21,1,2,self))

    	

##    	self.loop = "outer"
##    	self.sent_to_weigh = False
##    	self.slowed_to_stop = False
##        print("Setting turnout for initial")
##    	os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 19")
##        time.sleep(0.3)
##        print("Setting turnout 2 for initial")
##    	os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 6")
##        time.sleep(0.3)
##        os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 5")
##        time.sleep(0.3)
##        os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 20")
##
##        print("Setting initial speed")
##    	#os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py 1 0.5")
    os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 13")

    def activated(self, channel, pin_id, left_block, right_block):
    	print("Activated: " + str(pin_id))
    	if(pin_id == 16):
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 6")
        elif(pin_id == 6):
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 26")
        elif(pin_id == 21):
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 13")


BeamBreakerBank()
while True:
    #print("Waiting")
    time.sleep(0.1)
