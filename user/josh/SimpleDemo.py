import RPi.GPIO as GPIO, time
import datetime
import os

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        print("Time since last activation: " + str(channel) + ": " + str(datetime.datetime.utcnow()-self.time_of_last_break))
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

    	self.loop = "outer"
    	self.sent_to_weigh = False
    	self.slowed_to_stop = False
        print("Setting turnout for initial")
    	#os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 19")
        time.sleep(0.3)
        print("Setting turnout 2 for initial")
    	#os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 6")
        time.sleep(0.3)
        #os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 5")
        time.sleep(0.3)
        #os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 20")

        print("Setting initial speed")
    	#os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py 1 0.5")
	
    	# Set up beam breakers, change if you change the ports for
    	#  the beam breakers or add more (need to fix blocks).
    	#  Blocks determined by counter-clockwise orientation.
##    	self.beam_breaker.append(BeamBreaker(18,1,2,self))
##        self.beam_breaker.append(BeamBreaker(4,1,2,self))
##    	self.beam_breaker.append(BeamBreaker(26,1,2,self))
    	self.beam_breaker.append(BeamBreaker(12,1,2,self))
    	self.beam_breaker.append(BeamBreaker(16,1,2,self))
    	self.beam_breaker.append(BeamBreaker(26,1,2,self))
    	#self.beam_breaker.append(BeamBreaker(21,1,2,self))


    def activated(self, channel, pin_id, left_block, right_block):
    	#STOP Beam breakers?
	print("Activated: " + str(pin_id))
    	if(pin_id == 12):
            self.sent_to_weigh = False
            self.slowed_to_stop = False
            if(self.loop == "outer"):
                #Make loop inner
                self.loop = "inner"
                print("Setting loop to inner")
                os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 13")
            elif(self.loop == "inner"):
                #Make loop outer
                self.loop = "outer"
                print("Setting loop to outer")
                os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 6")
        elif(pin_id == 16):
            if(self.sent_to_weigh == False):
                self.sent_to_weigh = True
                #Swtich turnout to go to weight
                print("Setting turnout to go to weigh station")
                #os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 13")
                #Change train to reverse direction
                print("Changing train direction")
                #os.system("python /home/pi/teamge/user/Matt/changeDirectionOfficial.py 1")
        elif(pin_id == 26):
            if(self.slowed_to_stop == False):
                self.slowed_to_stop = True
                print("Slowing to a stop")
                #os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py 1 0.0")
                #time.sleep(1)
                print("Changing direction")
                #os.system("python /home/pi/teamge/user/Matt/changeDirectionOfficial.py 1")
                print("Speeding up the train")
                #os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py 1 0.5")
        elif(pin_id == 21):
            print("stopping train")
            #os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py 1 0.0")
            print("shutting off track power")
            #os.system("python /home/pi/teamge/user/Matt/turnTrackOffOfficial.py")
	#START beam breakers?

BeamBreakerBank()
while True:
    #print("Waiting")
    time.sleep(0.1)
