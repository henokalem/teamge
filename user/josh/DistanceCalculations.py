import RPi.GPIO as GPIO, time
import datetime

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        time = datetime.datetime.utcnow()
        print("Time since last activation: " + str(datetime.datetime.utcnow()-self.time_of_last_break))
        if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time:
            #Call activated function
            self.beam_breaker_bank.activated(channel, self.pin_id, time)
        else:
            #Time was too short, was same train
            print("The same train activated the beam break! ID: ", self.pin_id)
        self.time_of_last_break = datetime.datetime.utcnow()

    #Constructor
    # Left and right blocks determined by Couner-clockwise orienation
    def __init__(self, breaker_id, pin_id, beam_breaker_bank):
        self.pin_id = pin_id
        self.breaker_id = breaker_id
        self.beam_breaker_bank = beam_breaker_bank
        self.wait_time = 3
        self.time_of_last_break = datetime.datetime.utcnow()

        # Set up the initial GPIO pin ouputs
        GPIO.setup(self.pin_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin_id, GPIO.FALLING, callback=self.beamBroken, bouncetime=200)

# Class for holding all of the beam breakers
class BeamBreakerBank:
    # Constructor
    def __init__(self):
        self.beam_breaker = []
        self.trains = []
        
        self.pairs = []
        self.last_hit = None
        self.last_time = None

        #Set up initial GPIO settings
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Set up beam breakers, change if you change the ports for
        #  the beam breakers or add more (need to fix blocks).
        #  Blocks determined by counter-clockwise orientation.
        self.beam_breaker.append(BeamBreaker(7,21,self))
    	self.beam_breaker.append(BeamBreaker(8,20,self))
    	self.beam_breaker.append(BeamBreaker(9,16,self))
        #self.beam_breaker.append(BeamBreaker(12,self))
    	self.beam_breaker.append(BeamBreaker(2,26,self))
    	#self.beam_breaker.append(BeamBreaker(19,self))
    	self.beam_breaker.append(BeamBreaker(1,13,self))
    	self.beam_breaker.append(BeamBreaker(4,6,self))
    	self.beam_breaker.append(BeamBreaker(5,5,self))

        # Set up the trains
        self.trains.append(Train(1, 1))

        # Set up the pairs
        self.pairs.append(Pair(2,8))
        self.pairs.append(Pair(2,9))
        self.pairs.append(Pair(2,1))
        self.pairs.append(Pair(9,5))
        self.pairs.append(Pair(5,1))
        self.pairs.append(Pair(1,4))
        self.pairs.append(Pair(4,7))
        self.pairs.append(Pair(4,8))
        self.pairs.append(Pair(4,2))
##        self.pairs.append(Pair(2,3))
##        self.pairs.append(Pair(3,6))
##        self.pairs.append(Pair(6,9))

    def activated(self, channel, pin_id, time_of_break):
        breaker_id = None
        for breaker in self.beam_breaker:
            if breaker.pin_id == pin_id:
                breaker_id = breaker.breaker_id
                break

        if breaker_id == None:
            print("Shit")
        
        print("Activated: " + str(pin_id) + ", Breaker Number: " + str(breaker_id))

        if(self.last_hit == None):
            print("Initializing")
        else:
            temp = Pair(self.last_hit,breaker_id)
            elapsed_time = (time_of_break - self.last_time).total_seconds()
            for pair in self.pairs:
                if(pair.compare(temp)):
                    pair.average = float(pair.average*pair.num + elapsed_time) / float(pair.num + 1)
                    pair.num = pair.num + 1
                    break
        self.last_hit = breaker_id
        self.last_time = time_of_break


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


class Pair:
    # Constructor
    def __init__(self, num_1, num_2):
        self.GPIO1 = num_1
        self.GPIO2 = num_2
        self.num = 0
        self.average = 0

    def compare(self, pair):
        if(self.GPIO1 == pair.GPIO1):
            if(self.GPIO2 == pair.GPIO2):
                return True
        elif(self.GPIO1 == pair.GPIO2):
            if(self.GPIO2 == pair.GPIO1):
                return True
        return False


bank=BeamBreakerBank()
print("started")
toContinue = True
while toContinue:
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        #Perform distance calculations here
        pair1 = int(input("Input calculated pair x: "))
        pair2 = int(input("Input calculated pair y: "))
        dist = float(input("Input distance between pair: "))
        speed = 0
        temp = Pair(pair1,pair2)
        for pair in bank.pairs:
            if(pair.compare(temp)):
                #Calculate approx. speed of train
                speed = dist/pair.average
                break
        print("Approximate train speed: " + str(speed))
        for pair in bank.pairs:
            print("Distance between " + str(pair.GPIO1) + " and " + str(pair.GPIO2) + " is " + str(speed*pair.average))
        toContinue = False
            

