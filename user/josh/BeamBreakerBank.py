import RPi.GPIO as GPIO, time
import datetime

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        print("Time since last activation: " + str(datetime.datetime.utcnow()-self.time_of_last_break))
        if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time:
            #Call activated function
            self.beam_breaker_bank.activated(channel, self.pin_id, self.left_block, self.right_block, datetime.datetime.utcnow())
        else:
            #Time was too short, was same train
            print("The same train activated the beam break! ID: ", self.pin_id)
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
    	self.dist_pairs = []
	
    	# Set up beam breakers, change if you change the ports for
    	#  the beam breakers or add more (need to fix blocks).
    	#  Blocks determined by counter-clockwise orientation.
    	self.beam_breaker.append(BeamBreaker(5,6,4,self))
    	self.beam_breaker.append(BeamBreaker(6,6,5,self))
    	self.beam_breaker.append(BeamBreaker(19,4,1,self))
    	self.beam_breaker.append(BeamBreaker(20,5,1,self))
    	self.beam_breaker.append(BeamBreaker(12,1,2,self))
    	self.beam_breaker.append(BeamBreaker(26,3,2,self))
    	self.beam_breaker.append(BeamBreaker(21,2,6,self))
    	self.beam_breaker.append(BeamBreaker(16,2,4,self))
    	self.beam_breaker.append(BeamBreaker(13,2,2,self))

    	# Set up the trains
    	self.trains.append(Train(1, 2))

    	# Set up distances
    	self.dist_pairs.append(BreakerPair(25,12,24.984))
    	self.dist_pairs.append(BreakerPair(18,12,21.925))
    	self.dist_pairs.append(BreakerPair(6,25,24.482))
    	self.dist_pairs.append(BreakerPair(18,5,16.398))
    	self.dist_pairs.append(BreakerPair(5,24,35.380))
    	self.dist_pairs.append(BreakerPair(6,24,34.713))
    	self.dist_pairs.append(BreakerPair(12,24,50.611))
    	self.dist_pairs.append(BreakerPair(18,23,15.004))
    	self.dist_pairs.append(BreakerPair(12,23,66.573))
    	self.dist_pairs.append(BreakerPair(26,23,14.343))

    def activated(self, channel, pin_id, left_block, right_block, time):
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
                if(train.speed_set == False):
                    train.direction = "counter-clockwise"
                    #train.speed_set = True
            else:
                # current block must equal right block, so moving into left block
                train.current_block = left_block
                if(train.speed_set == False):
                    train.direction = "clockwise"
                    #train.speed_set = True
            #Set time of last break and last beam breaker hit after determining speed
            if(train.last_breaker == None):
                print("Initializing")
            else:
                #Make temp breaker pair object, distance irrelevant
                temp = BreakerPair(train.last_breaker,pin_id,0)
                for pair in self.dist_pairs:
                    if(pair.compare(temp)):
                        print pair.distance
                        dist = pair.distance
                        elapsed_time = time - train.time_of_last_break
                        train.speed = dist/elapsed_time.total_seconds()
                        print("Speed: " + str(dist/elapsed_time.total_seconds()))
                        break
            train.last_breaker = pin_id
            train.time_of_last_break = time
            print(train)        
        elif len(potential_trains) >= 2:
            print("Too many trains could have set this off, cannot determine source.")

# Class for the trains
class Train:
    # Constructor
    def __init__(self, name, initial_block):
        self.name = name
        self.current_block = initial_block
        self.last_breaker = None
        self.direction = None
        self.speed_set = False
        self.speed = None
        self.time_of_last_break = None

    def __str__(self):
        return "Train " + str(self.name) + ", current block: " + str(self.current_block) + ", direction: " + str(self.direction) + ", speed: " + str(self.speed)
    def __repr__(self):
        return "Train " + str(self.name) + ", current block: " + str(self.current_block) + ", direction: " + str(self.direction) + ", speed: " + str(self.speed)

class BreakerPair:
    # Constructor
    def __init__(self, num_1, num_2, distance):
        self.GPIO1 = num_1
        self.GPIO2 = num_2
        self.distance = distance

    def compare(self, pair):
        if(self.GPIO1 == pair.GPIO1):
            if(self.GPIO2 == pair.GPIO2):
                return True
        elif(self.GPIO1 == pair.GPIO2):
            if(self.GPIO2 == pair.GPIO1):
                return True
        return False

BeamBreakerBank()
while True:
    #print("Waiting")
    time.sleep(0.1)
