import RPi.GPIO as GPIO, time
import datetime
import os

#Class for beam breakers
class BeamBreaker:
    def beamBroken(self,channel):
        time = datetime.datetime.utcnow()
        print("Time since last activation: " + str(datetime.datetime.utcnow()-self.time_of_last_break))
        if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time:
            #Call breakerActivated function
            self.beam_breaker_bank.breakerActivated(channel, self.pin_id, self, time)
        else:
            #Time was too short, was same train
            print("The same train activated the beam break! ID: ", self.pin_id)
        self.time_of_last_break = datetime.datetime.utcnow()

    #Constructor
    # Left and right blocks determined by Couner-clockwise orienation
    def __init__(self, breaker_id, pin_id, left_segment, right_segment, block, beam_breaker_bank):
        self.pin_id = pin_id
        self.breaker_id = breaker_id
        self.block = block
        self.beam_breaker_bank = beam_breaker_bank
        self.left_segment = left_segment
        self.right_segment = right_segment
        self.wait_time = 1
        self.time_of_last_break = datetime.datetime.utcnow()

        # Set up the initial GPIO pin ouputs
        GPIO.setup(self.pin_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin_id, GPIO.FALLING, callback=self.beamBroken, bouncetime=200)

# Class for holding all of the beam breakers
class TrainLayout:
    # Constructor
    def __init__(self):
        self.beam_breakers = []
        self.trains = []
        self.turnouts = []
        self.blocks = []
        self.pairs = []

        #Set up initial GPIO settings
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Initialize turnouts, blocks, trains, and breakers here
        self.turnouts.append(Turnout(1,20,21))
        self.turnouts.append(Turnout(2,5,7))
        self.turnouts.append(Turnout(3,12,16))
        self.turnouts.append(Turnout(4,19,26))
        self.turnouts.append(Turnout(5,6,13))

        #                            LBS  LBT  TL   RBS  RBT  TR
        self.blocks.append(Block(1,12.875,None,None,None,None,None,self.turnouts[5-1]))
        self.blocks.append(Block(2,38.9375,self.blocks[1-1],None,None,None,None,None))
        self.blocks.append(Block(3,27.5,self.blocks[2-1],None,None,None,None,self.turnouts[1-1]))
        self.blocks.append(Block(4,-1,self.blocks[3-1],None,None,None,None,None))
        self.blocks.append(Block(5,-1,self.blocks[4-1],None,None,None,None,None))
        self.blocks.append(Block(6,22.4375,self.blocks[5-1],None,None,None,None,None))
        self.blocks.append(Block(7,4.625,self.blocks[6-1],None,self.turnouts[4-1],self.blocks[1-1],None,None))
        self.blocks.append(Block(8,38.875,self.blocks[1-1],None,None,None,None,None))
        self.blocks.append(Block(9,5.125,self.blocks[8-1],None,None,None,None,None))
        self.blocks.append(Block(10,10.5625,self.blocks[9-1],None,self.turnouts[3-1],None,None,None))
        self.blocks.append(Block(11,7.375,self.blocks[10-1],None,None,None,None,None))
        self.blocks.append(Block(12,5.5,None,self.blocks[11-1],self.turnouts[2-1],None,None,None))
        self.blocks.append(Block(13,17.8125,self.blocks[12-1],None,None,self.blocks[7-1],None,None))
        self.blocks.append(Block(14,6.3125,self.blocks[3-1],None,None,None,None,None))
        self.blocks.append(Block(15,10.125,self.blocks[14-1],None,None,self.blocks[12-1],None,None))
        self.blocks.append(Block(16,-1,None,None,None,None,None,None))
        self.blocks.append(Block(17,-1,self.blocks[16-1],None,None,self.blocks[10-1],None,None))
        #Initialize the rest of the block connections here
        self.blocks[1-1].addRightStraight(self.blocks[2-1])
        self.blocks[1-1].addRightTurn(self.blocks[8-1])
        self.blocks[3-1].addRightStraight(self.blocks[4-1])
        self.blocks[3-1].addRightTurn(self.blocks[14-1])
        self.blocks[6-1].addRightStraight(self.blocks[7-1])
        self.blocks[7-1].addLeftTurn(self.blocks[13-1])
        self.blocks[9-1].addRightStraight(self.blocks[10-1])
        self.blocks[10-1].addLeftTurn(self.blocks[17-1])
        self.blocks[11-1].addRightStraight(self.blocks[12-1])
        self.blocks[12-1].addLeftStraight(self.blocks[15-1])

        for block in self.blocks:
            print(block)

        # Set up the pairs
        self.pairs.append(Pair(2,8,51.75))
        self.pairs.append(Pair(2,9,51.8125))
        self.pairs.append(Pair(2,1,22.4375))
        self.pairs.append(Pair(9,5,33.8125))
        self.pairs.append(Pair(5,1,15.625))
        self.pairs.append(Pair(1,4,12.875))
        self.pairs.append(Pair(4,7,D))
        self.pairs.append(Pair(4,8,15.6875))
        self.pairs.append(Pair(9,6,D))
        self.pairs.append(Pair(6,3,D))
        self.pairs.append(Pair(3,2,27.0625))

        self.beam_breakers.append(BeamBreaker(1,13,6,4,self.blocks[13-1],self))
        self.beam_breakers.append(BeamBreaker(2,26,4,1,self.blocks[1-1],self))
        self.beam_breakers.append(BeamBreaker(3,19,3,4,self.blocks[6-1],self))
        self.beam_breakers.append(BeamBreaker(4,6,5,6,self.blocks[11-1],self))
        self.beam_breakers.append(BeamBreaker(5,5,2,6,self.blocks[15-1],self))
        self.beam_breakers.append(BeamBreaker(6,12,2,3,self.blocks[5-1],self))
        self.beam_breakers.append(BeamBreaker(7,21,7,5,self.blocks[17-1],self))
        self.beam_breakers.append(BeamBreaker(8,20,1,5,self.blocks[9-1],self))
        self.beam_breakers.append(BeamBreaker(9,16,1,2,self.blocks[3-1],self))

        self.trains.append(Train(1,1))

    def breakerActivated(self, channel, pin_id, breaker, time_of_break):
        print("Activated: " + str(pin_id))

        #Code for on activation
        #See if trains are all initialized
        initialized = True
        for train in self.trains:
            if train.initialized == False:
                initialized = False
                break
        if(initialized == False):
            availble_trains = []
            for train in self.trains:
                if(train.current_segment == breaker.left_segment or train.current_segment == breaker.right_segment):
                    available_trains.append(train)
            if(len(available_trains)==1):
                if(available_trains[0].last_breaker_hit == None):
                    #Calculate direction
                    available_trains[0].last_breaker_hit = breaker.breaker_id
                    available_trains[0].time_of_last_hit = time_of_break
                    if(available_trains[0].current_segment == breaker.left_segment):
                        available_trains[0].direction = "clockwise"
                        available_trains[0].current_segment = breaker.right_segment
                    elif(available_trains[0].current_segment == breaker.right_segment):
                        available_trains[0].direction = "counter-clockwise"
                        available_trains[0].current_segment = breaker.left_segment
                elif(available_trains[0].last_breaker_hit != None and available_trains[0].speed == None):
                    #Calculate speed
                    distance = 0
                    temp = Pair(available_trains[0].last_breaker_hit,breaker.breaker_id)
                    for pair in self.pairs:
                        if(pair.compare(temp)):
                            distance = pair.distance
                            break
                    available_trains[0].speed = distance/((time_of_break-available_trains[0].time_of_last_break).total_seconds())
                    # Calculate block, beam breakers are all at distance 0 in their respective block
                    available_trains[0].current_block = breaker.block
                    available_trains[0].distance_in_block = 0
                    #Set as initialized
                    available_trains[0].initialized = True
                    # Set last hit breaker and time
                    available_trains[0].last_breaker_hit = breaker.breaker_id
                    available_trains[0].time_of_last_hit = time_of_break
        #After if block

        #Check for trains in neighboring blocks
        available_trains = []
        for train in self.trains:
            if(train.current_block == breaker.block or train.current_block == breaker.block.left_straight_block):
                availble_trains.append(train)
        if(len(available_trains) == 0):
            print("No train could have set this off!")
        else:
            print("Train set this off")
           
        
            

# Class for a block object
class Block:
    # Constructor
    def __init__(self, block_id, distance, left_block_straight, left_block_turn, turnout_left, right_block_straight, right_block_turn, turnout_right):
        self.block_id = block_id
        self.distance = distance
        self.left_block_straight = left_block_straight
        self.left_block_turn = left_block_turn
        self.turnout_left = turnout_left
        self.right_block_straight = right_block_straight
        self.right_block_turn = right_block_turn
        self.turnout_right = turnout_right

        if(self.turnout_left == None and self.left_block_straight != None and self.left_block_straight.turnout_right == None):
            self.left_block_straight.right_block_straight = self

        if(self.turnout_right == None and self.right_block_straight != None and self.right_block_straight.turnout_left == None):
            self.right_block_straight.left_block_straight = self

    def addLeftTurn(self, left_block_turn):
        self.left_block_turn = left_block_turn

    def addRightTurn(self, right_block_turn):
        self.right_block_turn = right_block_turn

    def addLeftStraight(self, left_block_straight):
        self.left_block_straight = left_block_straight

    def addRightStraight(self, right_block_straight):
        self.right_block_straight = right_block_straight

    def __str__(self):
        print_string = "Block: " + str(self.block_id)
        print_string += " Distance: " + str(self.distance)
        if(self.left_block_straight!=None):
            print_string += " Left Block Straight: " + str(self.left_block_straight.block_id)
        if(self.right_block_straight!=None):
            print_string += " Right Block Straight: " + str(self.right_block_straight.block_id)
        if(self.left_block_turn!=None):
            print_string += " Left Block Turn: " + str(self.left_block_turn.block_id)
        if(self.right_block_turn!=None):
            print_string += " Right Block Turn: " + str(self.right_block_turn.block_id)
        if(self.turnout_left!=None):
            print_string += " Left Turnout: " + str(self.turnout_left.turnout_id)
        if(self.turnout_right!=None):
            print_string += " Right Turnout: " + str(self.turnout_right.turnout_id)
        return print_string

class Pair:
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

# Class for the train object
class Train:
    # Constructor
    def __init__(self, train_id, starting_segment):
        self.current_segment = starting_segment
        self.current_block = None
        self.last_breaker_hit = None
        self.time_of_last_hit = None
        self.train_id = train_id
        self.distance_in_block = None
        self.speed = None
        self.direction = None
        self.initialized = False

# Class for controlling turnouts
class Turnout:
    # Constructor
    def __init__(self, turnout_id, straight_pin_num, turn_pin_num):
        self.turnout_id = turnout_id
        self.straight_pin_num = straight_pin_num
        self.turn_pin_num = turn_pin_num
        self.current_state = "straight"
        self.pi2IP = "10.0.1.48"

        # set up the initial GPIO pin outputs
        GPIO.setup(self.straight_pin_num, GPIO.OUT)
        GPIO.output(self.straight_pin_num, GPIO.LOW)
        GPIO.setup(self.turn_pin_num, GPIO.OUT)
        GPIO.output(self.turn_pin_num, GPIO.LOW)

        # Send signal to make physical turnout to straight
        time.sleep(2)
        self.__activateRelay(self.straight_pin_num)

    # Put the turnout in the straight state
    def activateStraight(self):
        if self.current_state == "straight":
            print("Turnout is already in the 'straight' state")
        else:
            self.current_state = "straight"
            print("Putting turnout in 'straight' state")
            self.__activateRelay(self.straight_pin_num)

    # Put the turnout in the turned state
    def activateTurn(self):
        if self.current_state == "turn":
            print("Turnout is already in the 'turned' state")
        else:
            self.current_state = "turn"
            print("Putting turnout in 'turn' state")
            self.__activateRelay(self.turn_pin_num)
            
    # send the signal to activate the correct pin on the pi
    def __activateRelay(self, pin_num, time_delay=0.4):
        #Activate the pin for the duration of the time delay, then shut off
        print("ACTIVATING")
        os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py " + self.pi2IP + " " + str(pin_num))
        # CALL: the os.execute file that will send signal to activate correct relay


bank=TrainLayout()
print("started")

