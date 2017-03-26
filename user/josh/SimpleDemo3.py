import RPi.GPIO as GPIO, time
import datetime
import os

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        print("Time since last activation: " + str(channel) + ": " + str(datetime.datetime.utcnow()-self.time_of_last_break))
        if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time:
            #Call activated function
            self.beam_breaker_bank.activated(channel, self.pin_id)
        else:
            #Time was too short, was same train
            print("The same train activated the beam break!")
        self.time_of_last_break = datetime.datetime.utcnow()

    #Constructor
    # Left and righ blocks determined by Couner-clockwise orienation
    def __init__(self, pin_id, beam_breaker_bank):
        self.pin_id = pin_id
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

    	self.turn = 0

    	# Set up beam breakers, change if you change the ports for
    	#  the beam breakers or add more (need to fix blocks).
    	#  Blocks determined by counter-clockwise orientation.
    	self.beam_breaker.append(BeamBreaker(5,self))


    def activated(self, channel, pin_id):
	print("Activated: " + str(pin_id))
	if(self.turn == 0):
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 6")
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 19")
            #Set to middle loop
            self.turn = (self.turn + 1) % 3
        elif(self.turn == 1):
            #Set to Outer loop
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 26")
            self.turn = (self.turn + 1) % 3
        elif(self.turn == 2):
            #Set to inner loop
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py 10.0.1.48 13")
            self.turn = (self.turn + 1) % 3
        print self.turn

BeamBreakerBank()
while True:
    #print("Waiting")
    time.sleep(0.1)
