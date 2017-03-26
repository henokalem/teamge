import RPi.GPIO as GPIO, time
import MFRC522
import signal
import datetime
import sys
import os

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        #print("Time since last activation: " + str(channel) + ": " + str(datetime.datetime.utcnow()-self.time_of_last_break))
        if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time:
            #Call activated function
            self.beam_breaker_bank.activated(channel, self.pin_id)
        #else:
            #Time was too short, was same train
            #print("The same train activated the beam break!")
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
        #GPIO.setmode(GPIO.BCM)
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
    	self.beam_breaker.append(BeamBreaker(29,self))
    	#os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py")


    def activated(self, channel, pin_id):
        #IP address for the pi 2 so we can easily change it
        pi2IP = "35.12.215.95"
	print("Activated: " + str(pin_id))
	if(self.turn == 0):
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py " + pi2IP + " 6,19,r")
            #os.system("sudo python /home/pi/teamge/user/Matt/setRed.py")
            #Set to middle loop
            self.turn = (self.turn + 1) % 3
        elif(self.turn == 1):
            #Set to Outer loop
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py " + pi2IP + " 26,g")
            #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
            self.turn = (self.turn + 1) % 3
        elif(self.turn == 2):
            #Set to inner loop
            os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py " + pi2IP + " 13,y")
            #os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py")
            self.turn = (self.turn + 1) % 3
        #print self.turn

BeamBreakerBank()
while True:
    #print("Waiting")
    time.sleep(0.05)
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        id = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])

	if id == "13642342" or id == "13643842":
	    print("Train 1 Passed")
	elif id == "136412043" or id == "136423144":
	    print("Train 2 Passed")
