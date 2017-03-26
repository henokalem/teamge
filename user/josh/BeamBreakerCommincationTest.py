import RPi.GPIO as GPIO, time
import datetime
import socket   
import sys  
import struct

#This is indiciating if beam breakers are active
globalVar = True

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        global globalVar
        if(globalVar):
            print("Time since last activation: " + str(datetime.datetime.utcnow()-self.time_of_last_break))
            if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time:
                #Call activated function
                self.beam_breaker_bank.activated(channel, self.pin_id)
            else:
                #Time was too short, was same train
                print("The same train activated the beam break! ID: ", self.pin_id)
            self.time_of_last_break = datetime.datetime.utcnow()
        else:
            print "activation of " + str(channel) + " was ignored"

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
	
    	# Set up beam breakers, change if you change the ports for
    	#  the beam breakers or add more (need to fix blocks).
    	#  Blocks determined by counter-clockwise orientation.
    	self.beam_breaker.append(BeamBreaker(21,self))
    	self.beam_breaker.append(BeamBreaker(20,self))
    	self.beam_breaker.append(BeamBreaker(16,self))
    	self.beam_breaker.append(BeamBreaker(12,self))
    	self.beam_breaker.append(BeamBreaker(19,self))
    	self.beam_breaker.append(BeamBreaker(13,self))
    	self.beam_breaker.append(BeamBreaker(5,self))
    	self.beam_breaker.append(BeamBreaker(6,self))
    	self.beam_breaker.append(BeamBreaker(26,self))


    	# Set up the trains
##    	self.trains.append(Train(1, 1))

    def activated(self, channel, pin_id):
    	print("Activated: " + str(pin_id))
    	sendMessage('10.0.1.48',5)

#####################################################

#main function
def sendMessage(hostname, pin):


    host = hostname
    port = 8888


    #create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()

    print 'Socket Created'

    try:
        remote_ip = socket.gethostbyname( host )
        s.connect((host, port))

    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

    print 'Socket Connected to ' + host + ' on ip ' + remote_ip

    #Send some data to remote server
    message = str(pin)

    try :
        global globalVar
        globalVar = False
        #Set the whole string
        #while True:
        s.send(message)
        print 'Message sent successfully'
            #print 'Closing socket'
            #s.close()
            #sys.exit()
    ##        time.sleep(1)
    ##        print 'Sending...'
            #get reply and print
            #print recv_timeout(s)
        recieve = s.recv(1024)
        while(recieve != "Completed"):
            if(recieve != ""):
                print recieve
            recieve = s.recv(1024)
        print recieve
        print 'Closing Socket'
        s.close()
        globalVar = True
        #sys.exit()
            
            #break
    except socket.error:
        #Send failed
        print 'Send failed'
        globalVar = True
        #sys.exit()


BeamBreakerBank()
while True:
    #print("Spinning")
    print("Waiting")
    print globalVar
    time.sleep(0.1)
