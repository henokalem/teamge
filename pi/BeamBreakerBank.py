import RPi.GPIO as GPIO, time
import datetime

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        print("Time since last activation: " + str(datetime.datetime.utcnow()-self.time_of_last_break))
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
    	self.beam_breaker.append(BeamBreaker(3,2,1,self))
    	self.beam_breaker.append(BeamBreaker(2,1,2,self))

    	# Set up the trains
    	self.trains.append(Train(1, 1))

    def activated(self, channel, pin_id, left_block, right_block):
    	print("Activated: " + str(pin_id))

    	# Logic for sensor activation
    	potential_trains = []
    	for train in self.trains:
            if (train.current_block == left_block) or (train.current_block == right_block):
                potential_trains.append(train)
        if len(potential_trains) == 0:
            print("No train could have set this off!")
        elif len(potential_trains) == 1:
            # Peform operation here to move blocks
            train = potential_trains[0]
            if (train.current_block == left_block):
                #This means it is moving from left to right block
                train.current_block = right_block
                #Set direction here?
                print(train)
            else:
                # current block must equal right block, so moving into left block
                train.current_block = left_block
                print(train)
        elif len(potential_trains) >= 2:
            print("Too many trains could have set this off, cannot determine source.")

# Class for the trains
class Train:
    # Constructor
    def __init__(self, name, initial_block):
        self.name = name
        self.current_block = initial_block

    def __str__(self):
        return "Train " + str(self.name) + ", current block: " + str(self.current_block)
    def __repr__(self):
        return "Train " + str(self.name) + ", current block: " + str(self.current_block)

BeamBreakerBank()
while True:
    #print("Waiting")
    time.sleep(0.1)
