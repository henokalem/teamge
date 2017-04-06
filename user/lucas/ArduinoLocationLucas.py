import serial
import string
import time
import RPi.GPIO as GPIO, time
import datetime
import os
import csv
import sys


#Class for beam breakers
class BeamBreaker:
    def beamBroken(self):
        time = datetime.datetime.utcnow()
        if (time-self.beam_breaker_bank.time_since_start).total_seconds() < 10:
            print("Time since program start: " + str((time-self.beam_breaker_bank.time_since_start).total_seconds()))
        #print("Time since last activation: " + str(datetime.datetime.utcnow()-self.time_of_last_break))
        #Test to see if the beam breaker has not been hit in the last WAIT_TIME amount of seconds, and that it has gone off at least 3
        #seconds after the program started (which avoids the beginning noise from when first reading from aruduino)
        if (datetime.datetime.utcnow() - self.time_of_last_break).total_seconds() > self.wait_time and (time-self.beam_breaker_bank.time_since_start).total_seconds() > 10:
            #Call breakerActivated function
            self.beam_breaker_bank.breakerActivated(self, time)
        else:
            #Time was too short, was same train
            #print("The same train activated the beam break! ID: ", self.breaker_id)
            a=2
        self.time_of_last_break = datetime.datetime.utcnow()

    #Constructor
    # Left and right blocks determined by Couner-clockwise orienation
    def __init__(self, breaker_id, left_segment, right_segment, block, beam_breaker_bank):
        self.breaker_id = breaker_id
        self.block = block
        self.beam_breaker_bank = beam_breaker_bank
        self.left_segment = left_segment
        self.right_segment = right_segment
        self.wait_time = 1
        self.time_of_last_break = datetime.datetime.utcnow()

# Class for holding all of the beam breakers
class TrainLayout:
    # Constructor
    def __init__(self,train1_start_segment,train2_start_segment):
        #Constants
        self.TRAIN_CHECK_DIST = 6
        self.LAG_TIME = 1
        self.COLLISION_TIME_BUFFER = 5
        self.TRAIN_DISTANCE_BUFFER = 15
        self.TURNOUT_COLLISION_TIME_BUFFER = 1.5
        self.FIX_TIME_BUFFER = 0.1

        self.breaker_8_offset = 0
        self.state = 0
        
        self.beam_breakers = []
        self.trains = []
        self.turnouts = []
        self.blocks = []
        self.pairs = []
        self.time_since_start = datetime.datetime.utcnow()
        self.fix_time_remaining = 0
        self.time_of_last_check = datetime.datetime.utcnow()


        # Initialize turnouts, blocks, trains, and breakers here

        #print("Train 1 starting segment: " + str(train1_start_segment))
        #print("Train 2 starting segment: " + str(train2_start_segment))
        if(train1_start_segment != 0):
            self.trains.append(Train(1,train1_start_segment))
        if(train2_start_segment != 0):
            self.trains.append(Train(3,train2_start_segment))
        #print(len(self.trains))
        if(len(self.trains) == 0):
            print("There are no trains to keep track of!")
            sys.exit()


        
        self.turnouts.append(Turnout(1,20,21, "counter-clockwise"))
        time.sleep(1)
        self.turnouts.append(Turnout(2,5,7, "clockwise"))
        time.sleep(1)
        self.turnouts.append(Turnout(3,12,16, "clockwise"))
        time.sleep(1)
        self.turnouts.append(Turnout(4,19,26, "clockwise"))
        time.sleep(1)
        self.turnouts.append(Turnout(5,6,13, "counter-clockwise"))

        

        #Set up the initial blocks
        #                            LBS  LBT  TL   RBS  RBT  TR
        self.blocks.append(Block(1,12.875,None,None,None,None,None,self.turnouts[5-1]))
        self.blocks.append(Block(2,38.9375,self.blocks[1-1],None,None,None,None,None))
        self.blocks.append(Block(3,27.5,self.blocks[2-1],None,None,None,None,self.turnouts[1-1]))
        self.blocks.append(Block(4,6.3125,self.blocks[3-1],None,None,None,None,None))
        self.blocks.append(Block(5,23.125,self.blocks[4-1],None,None,None,None,None))
        self.blocks.append(Block(6,22.4375,self.blocks[5-1],None,None,None,None,None))
        self.blocks.append(Block(7,4.625,self.blocks[6-1],None,self.turnouts[4-1],self.blocks[1-1],None,None))
        self.blocks.append(Block(8,38.875 + self.breaker_8_offset,self.blocks[1-1],None,None,None,None,None))
        self.blocks.append(Block(9,5.125 - self.breaker_8_offset,self.blocks[8-1],None,None,None,None,None))
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

##        for block in self.blocks:
##            print(block)

        #Now that all blocks are defined, set up the turnout blocks
        self.turnouts[1-1].setBlock(self.blocks[3-1],self.blocks[3-1].distance)
        self.turnouts[2-1].setBlock(self.blocks[12-1],0)
        self.turnouts[3-1].setBlock(self.blocks[10-1],0)
        self.turnouts[4-1].setBlock(self.blocks[7-1],0)
        self.turnouts[5-1].setBlock(self.blocks[1-1],self.blocks[1-1].distance)

        # Set up the pairs
        # Pair are defined in a counter-clockwise order!!
        self.pairs.append(Pair(2,8,51.75+self.breaker_8_offset))
        self.pairs.append(Pair(2,9,51.8125))
        self.pairs.append(Pair(1,2,22.4375))
        self.pairs.append(Pair(9,5,33.8125))
        self.pairs.append(Pair(5,1,15.625))
        self.pairs.append(Pair(4,1,12.875))
        #self.pairs.append(Pair(4,7,D))
        self.pairs.append(Pair(8,4,15.6875-self.breaker_8_offset))
        self.pairs.append(Pair(9,6,33.8125))
        self.pairs.append(Pair(6,3,23.125))
        self.pairs.append(Pair(3,2,27.0625))
        # Other pairs for if a beam breaker fails
        self.pairs.append(Pair(8,1,28.5625-self.breaker_8_offset))
        self.pairs.append(Pair(2,4,67.4375))
        self.pairs.append(Pair(6,2,50.1875))
        self.pairs.append(Pair(1,8,74.1875+self.breaker_8_offset))
        self.pairs.append(Pair(3,8,78.8125+self.breaker_8_offset))
        self.pairs.append(Pair(1,9,74.25))
        self.pairs.append(Pair(3,9,78.875))
        self.pairs.append(Pair(8,2,51-self.breaker_8_offset))
        self.pairs.append(Pair(2,5,85.625))
        self.pairs.append(Pair(5,2,38.0625))
        self.pairs.append(Pair(4,8,87.0625+self.breaker_8_offset))
        self.pairs.append(Pair(4,2,35.3125))

        #Initialize beam breakers
        self.beam_breakers.append(BeamBreaker(1,6,4,self.blocks[13-1],self))
        self.beam_breakers.append(BeamBreaker(2,4,1,self.blocks[1-1],self))
        self.beam_breakers.append(BeamBreaker(3,3,4,self.blocks[6-1],self))
        self.beam_breakers.append(BeamBreaker(4,5,6,self.blocks[11-1],self))
        self.beam_breakers.append(BeamBreaker(5,2,6,self.blocks[15-1],self))
        self.beam_breakers.append(BeamBreaker(6,2,3,self.blocks[5-1],self))
        self.beam_breakers.append(BeamBreaker(7,7,5,self.blocks[17-1],self))
        self.beam_breakers.append(BeamBreaker(8,1,5,self.blocks[9-1],self))
        self.beam_breakers.append(BeamBreaker(9,1,2,self.blocks[3-1],self))

        #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")

        time.sleep(1)
        self.turnouts[5-1].activateTurn()
##        self.turnouts[4-1].activateTurn()
##        self.turnouts[2-1].activateTurn()
            

        # Get the initial SPROG speed setting from the file
        print "reading from file"
        try:
            f = open('/home/pi/teamge/user/josh/trainProperties.txt')
            try:
                reader = csv.reader(f)
                firstRow = True
                currentRow = 0
                for row in reader:
                    if(firstRow):
                        print "Reading from first row"
                        firstRow = False
                    else:
                        print "Reading from another row"
                        train_id = int(row[0])
                        train_speed = float(row[1])
                        for train in self.trains:
                            if train.train_id == train_id:
                                train.sprog_speed = train_speed
                                print("Setting Train " + str(train.train_id) + " to have SPROG speed: " + str(train.sprog_speed))
            finally:
                f.close()
        except IOError:
##            os.system("sudo python /home/pi/teamge/user/Matt/setRed.py")
            print("Could not open file")
        

    def activateBreaker(self, breaker_id):
        for breaker in self.beam_breakers:
            if breaker.breaker_id == breaker_id:
                breaker.beamBroken()
                break

    def updateTrains(self):
        for train in self.trains:
            if(train.initialized):
                train.updateTrain(datetime.datetime.utcnow())
                print("Train : " + str(train.train_id) + " Block: " + str(train.current_block.block_id) + " Location: " + str(train.distance_in_block) + " Speed: " + str(train.speed) + " Sprog Speed: " + str(train.sprog_speed))
        if len(self.trains) > 1:
            #Update fix time remaining
            elapsed_since_check = (datetime.datetime.utcnow()-self.time_of_last_check).total_seconds()
            #self.fix_time_remaining -= elapsed
            #print("Fix time remaining in update train: " + str(self.fix_time_remaining))
            if(self.fix_time_remaining < elapsed_since_check):
                self.fix_time_remaining = 0

            if self.trains[0].initialized != False and self.fix_time_remaining <= 0:
                #print("CHECKING COLLISIONS")
                self.checkForCollisions()
        # Insert code to send locations to html 

    def checkForCollisions(self):
        print("Checking for collision cases")
        #Only check the first train since there are only 2 trains, will do actions on either/both trains depending on what needs to be done
        checkTrain = self.trains[0]
        otherTrain = self.trains[1]
        #will be checking 40" in front and behind the train, so distance = 0 means at the train
        checkDistance = 40
        currentDistance = 0
        CCWArray = []
        CWArray = []

        # Check in the counter-clockwise direction
        if otherTrain.current_block == checkTrain.current_block and otherTrain.distance_in_block > checkTrain.distance_in_block and (otherTrain.distance_in_block - checkTrain.distance_in_block) < checkDistance:
            CCWArray.append((otherTrain, otherTrain.distance_in_block - checkTrain.distance_in_block))
        if checkDistance > checkTrain.current_block.distance - checkTrain.distance_in_block:
            checkDistance -= checkTrain.current_block.distance - checkTrain.distance_in_block
            currentDistance += checkTrain.current_block.distance - checkTrain.distance_in_block
            appendArray = self.checkBlockCCW(checkTrain.current_block.right_block_straight, checkDistance, currentDistance, otherTrain)
            CCWArray.extend(appendArray)
            if checkTrain.current_block.right_block_turn != None:
                CCWArray.append((checkTrain.current_block.turnout_right, checkTrain.current_block.distance - checkTrain.distance_in_block))
                appendArray = self.checkBlockCCW(checkTrain.current_block.right_block_turn, checkDistance, currentDistance, otherTrain)
                CCWArray.extend(appendArray)
        print(CCWArray)

        # Check in the clockwise direction
        checkDistance = 40
        currentDistance = 0

        if otherTrain.current_block == checkTrain.current_block and otherTrain.distance_in_block < checkTrain.distance_in_block and (checkTrain.distance_in_block - otherTrain.distance_in_block) < checkDistance:
            CWArray.append((otherTrain, checkTrain.distance_in_block - otherTrain.distance_in_block))
        if checkDistance > checkTrain.distance_in_block:
            checkDistance -= checkTrain.distance_in_block
            currentDistance += checkTrain.distance_in_block
            appendArray = self.checkBlockCW(checkTrain.current_block.left_block_straight, checkDistance, currentDistance, otherTrain)
            CWArray.extend(appendArray)
            if checkTrain.current_block.left_block_turn != None:
                CWArray.append((checkTrain.current_block.turnout_left, checkTrain.distance_in_block))
                appendArray = self.checkBlockCW(checkTrain.current_block.left_block_turn, checkDistance, currentDistance, otherTrain)
                CWArray.extend(appendArray)
        print(CWArray)


        # Check for collision conditions
        if(checkTrain.direction == otherTrain.direction and checkTrain.direction == "counter-clockwise"):
            print("Checking same direction counter-clockwise")
            self.sameDirectionCollisionChecks(CCWArray, CWArray, checkTrain)
        elif(checkTrain.direction == otherTrain.direction and checkTrain.direction == "clockwise"):
            print("Checking same direction clockwise")
            self.sameDirectionCollisionChecks(CWArray, CCWArray, checkTrain)
        else:
            print("Checking different directions")


    def checkBlockCCW(self, block, checkDist, currentDist, otherTrain):
        returnArray = []
        if block != None:
            if block.turnout_left != None:
                returnArray.append((block.turnout_left, currentDist))
            if otherTrain.current_block == block and otherTrain.distance_in_block < checkDist:
                returnArray.append((otherTrain, currentDist+otherTrain.distance_in_block))
            if checkDist > block.distance:
                checkDist -= block.distance
                currentDist += block.distance
                temp = self.checkBlockCCW(block.right_block_straight, checkDist, currentDist, otherTrain)
                returnArray.extend(temp)
                if block.turnout_right != None:
                    returnArray.append((block.turnout_right, currentDist))
                    temp = self.checkBlockCCW(block.right_block_turn, checkDist, currentDist, otherTrain)
                    returnArray.extend(temp)
        return returnArray

    def checkBlockCW(self, block, checkDist, currentDist, otherTrain):
        returnArray = []
        if block != None:
            if block.turnout_right != None:
                returnArray.append((block.turnout_right, currentDist))
            if otherTrain.current_block == block and block.distance-otherTrain.distance_in_block < checkDist:
                returnArray.append((otherTrain, currentDist+block.distance-otherTrain.distance_in_block))
            if checkDist > block.distance:
                checkDist -= block.distance
                currentDist += block.distance
                temp = self.checkBlockCW(block.left_block_straight, checkDist, currentDist, otherTrain)
                returnArray.extend(temp)
                if block.turnout_left != None:
                    returnArray.append((block.turnout_left, currentDist))
                    temp = self.checkBlockCW(block.left_block_turn, checkDist, currentDist, otherTrain)
                    returnArray.extend(temp)
        return returnArray
            
    def sameDirectionCollisionChecks(self, frontArray, backArray, checkTrain):
        #Check to see if other train is ahead or behind train, and use this to perform checks
        trainInFront = False
        trainInBack = False
        otherTrain = None
        otherTrainDist = None
        for distTuple in frontArray:
            if isinstance(distTuple[0], Train):
                otherTrain = distTuple[0]
                otherTrainDist = distTuple[1]
                trainInFront = True
        for distTuple in backArray:
            if isinstance(distTuple[0], Train):
                otherTrain = distTuple[0]
                otherTrainDist = distTuple[1]
                trainInBack = True
        #print("Front: " + str(trainInFront) + " Back: " + str(trainInBack))
                
        if(trainInBack == True):
            #Check to see if other train is faster, if not do nothing, no collision imminent
            if(otherTrain.speed > checkTrain.speed):
                #Second train faster, will eventually catch up.
                #Check to see if there is a direction-matching turnout between trains that we could switch
                for distTuple in backArray:
                    if distTuple[1] < otherTrainDist and isinstance(distTuple[0], Turnout) and distTuple[0].orientation == checkTrain.direction:
                        # Switch the Turnout if enough time before otherTrain reaches.
                        dist_between_train_and_turnout = otherTrainDist - distTuple[1]
                        time_to_reach = dist_between_train_and_turnout/abs(otherTrain.speed)
                        #Make sure time to reach is greater than lag time to change turnout
                        if(time_to_reach > self.LAG_TIME):
                            print("SWITCHING A TURNOUT: " + str(distTuple[0].turnout_id))
                            self.fix_time_remaining = time_to_reach
                            print("Fix time remaining: " + str(self.fix_time_remaining))
                            self.time_of_last_check = datetime.datetime.utcnow()
                            distTuple[0].switchState()
                            #found fix, ending method
                            return
                #If here, this means there was no turnout that could be swtiched in time
                # so see if time to collision is smaller than some margin, if so, slow down back train
                # or speed up front train
                time_to_collision = otherTrainDist/(otherTrain.speed - checkTrain.speed)
                if(time_to_collision < self.COLLISION_TIME_BUFFER or otherTrainDist <  self.TRAIN_DISTANCE_BUFFER):
                    #Slow down back train (other train) or speed up front train (check train)
                    print("Case: train is catching up and cannot swtich turnout in time")
                    if(otherTrain.sprog_speed > 0.5):
                        self.changeTrainSpeed(otherTrain,-0.2)
                        return
                    elif(checkTrain.sprog_speed < 0.9):
                        self.changeTrainSpeed(checkTrain,0.2)
                        return
                    

        elif(trainInFront == True):
            #Check to see if this train is faster, if not do nothing, no collision imminent
            if(otherTrain.speed < checkTrain.speed):
                #This train faster, will eventually catch up.
                #Check to see if there is a direction-matching turnout between trains that we could switch
                for distTuple in frontArray:
                    if distTuple[1] < otherTrainDist and isinstance(distTuple[0], Turnout) and distTuple[0].orientation == checkTrain.direction:
                        # Switch the Turnout if enough time before otherTrain reaches.
                        dist_between_train_and_turnout = distTuple[1]
                        time_to_reach = dist_between_train_and_turnout/abs(checkTrain.speed)
                        #Make sure time to reach is greater than lag time to change turnout
                        if(time_to_reach > self.LAG_TIME):
                            print("SETTING LIGHT TO YELLOW")
                            #os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py")
                            print("SWITCHING A TURNOUT: " + str(distTuple[0].turnout_id))
                            self.fix_time_remaining = time_to_reach
                            print("Fix time remaining: " + str(self.fix_time_remaining))
                            self.time_of_last_check = datetime.datetime.utcnow()
                            distTuple[0].switchState()
                            return
                #If here, this means there was no turnout that could be swtiched in time
                # so see if time to collision is smaller than some margin, if so, slow down back train
                # or speed up front train
                time_to_collision = otherTrainDist/(checkTrain.speed - otherTrain.speed)
                if(time_to_collision < self.COLLISION_TIME_BUFFER or otherTrainDist < self.TRAIN_DISTANCE_BUFFER):
                    #Slow down back train (other train) or speed up front train (check train)
                    print("Case: train is catching up and cannot swtich turnout in time")
                    if(checkTrain.sprog_speed > 0.5):
                        self.changeTrainSpeed(checkTrain,-0.2)
                        return
                    elif(otherTrain.sprog_speed < 0.9):
                        self.changeTrainSpeed(otherTrain,0.2)
                        return



        #traverse turnouts that are in opposite directions
        else:
            for distTuple in frontArray:
                if(isinstance(distTuple[0], Turnout) and distTuple[0].orientation != checkTrain.direction):
                    print("Checking for possible turnout collision")
                    turnout = distTuple[0]
                    ArrayStraight = []
                    ArrayTurn = []
                    if turnout.orientation == "clockwise":
                        checkDistance = 40
                        currentDistance = 0
                        ArrayStraight = self.processBlockForTrainCW(turnout.block.left_block_straight, checkDistance, currentDistance)
                        ArrayTurn = self.processBlockForTrainCW(turnout.block.left_block_turn, checkDistance, currentDistance)

                    elif turnout.orientation == "counter-clockwise":
                        checkDistance = 40
                        currentDistance = 0
                        ArrayStraight = self.processBlockForTrainCCW(turnout.block.right_block_straight, checkDistance, currentDistance)
                        ArrayTurn = self.processBlockForTrainCCW(turnout.block.right_block_turn, checkDistance, currentDistance)

                    if len(ArrayStraight) == 1 and len(ArrayTurn) == 1 and ArrayStraight[0][0].train_id != ArrayTurn[0][0].train_id:
                        train1 = ArrayStraight[0][0]
                        train2 = ArrayTurn[0][0]

                        train1Dist = ArrayStraight[0][1]
                        train2Dist = ArrayTurn[0][1]

                        train1TimeToTurnout = train1Dist / abs(train1.speed)
                        train2TimeToTurnout = train2Dist / abs(train2.speed)

                        if abs(train1TimeToTurnout - train2TimeToTurnout) <= self.TURNOUT_COLLISION_TIME_BUFFER:
                            #check distance of trains, either slow down train that will reach second or speed up train that will reach first
                            print("Case: Train collision possible at a turnout")
                            if(train1TimeToTurnout > train2TimeToTurnout):
                                #Train 1 will reach second, so try to slow train down
                                if(train1.sprog_speed > 0.5):
                                    #Slow down train1, by calculating appropriate change in sprog speed to prevent collision,
                                    # go down by 0.2 to prevent trains from having same sprog speed, keeps things interesting

                                    # Want to change speed so that train1TimeToTurnout - train2TimeToTurnout > self.TURNOUT_COLLISION_TIME_BUFFER
                                    print("-------------------------------------------------------------TESTING NEW SPROG SPEED----------------------")
                                    print("Train 1 slowing down?")
                                    speed_steps = train1.getSpeedStepsArray()
                                    print("Speed steps: " + str(speed_steps))
                                    curr_test_sprog_speed = train1.sprog_speed
                                    print("Current train sprog speed: " + str(curr_test_sprog_speed))
                                    speed_change_good = False
                                    new_speed_max = train1Dist / (self.TURNOUT_COLLISION_TIME_BUFFER + train2TimeToTurnout)
                                    print("New max speed we need: " + str(new_speed_max))
                                    while(curr_test_sprog_speed > 0.5 and speed_change_good == False):
                                        curr_test_sprog_speed -= 0.2
                                        print("Current testing sprog speed: " + str(curr_test_sprog_speed))
                                        new_approx_speed = speed_steps[int(curr_test_sprog_speed*10)]
                                        print("New approximate speed: " + str(new_approx_speed))
                                        if(new_approx_speed < new_speed_max):
                                            speed_change_good = True
                                    change_in_sprog_speed = curr_test_sprog_speed - train1.sprog_speed
                                    print("Calculated change in sprog speed: " + str(change_in_sprog_speed))
                                    print("---------------------------------------------------------END TESTING NEW SPROG SPEED----------------------")
                                    
                                    self.changeTrainSpeed(train1,change_in_sprog_speed)
                                    return # Stop looking for collisions, fix is in place
                                elif(train2.sprog_speed < 0.9):
                                    #Speed up train2

                                    print("-------------------------------------------------------------TESTING NEW SPROG SPEED----------------------")
                                    print("Train 2 speeding up?")
                                    speed_steps = train2.getSpeedStepsArray()
                                    print("Speed steps: " + str(speed_steps))
                                    curr_test_sprog_speed = train2.sprog_speed
                                    print("Current train sprog speed: " + str(curr_test_sprog_speed))
                                    speed_change_good = False
                                    new_speed_min = train2Dist / (train1TimeToTurnout - self.TURNOUT_COLLISION_TIME_BUFFER)
                                    while(curr_test_sprog_speed < 0.9 and speed_change_good == False):
                                        curr_test_sprog_speed += 0.2
                                        print("Current testing sprog speed: " + str(curr_test_sprog_speed))
                                        new_approx_speed = speed_steps[int(curr_test_sprog_speed*10)]
                                        print("New approximate speed: " + str(new_approx_speed))
                                        if(new_approx_speed > new_speed_min):
                                            speed_change_good = True
                                    change_in_sprog_speed = curr_test_sprog_speed - train2.sprog_speed
                                    print("Calculated change in sprog speed: " + str(change_in_sprog_speed))
                                    print("---------------------------------------------------------END TESTING NEW SPROG SPEED----------------------")
                                    
                                    self.changeTrainSpeed(train2,0.2)
                                    return # Stop looking for collisions, fix is in place
                                else:
                                    #This option means that train 1 cannot slow down, and train 2 cannot speed up
                                    # FIGURE OUT WHAT TO DO HERE
                                    print("CASE 3 FIX ME!")
                                    return # Stop looking for collisions, fix is in place
                            elif(train2TimeToTurnout > train1TimeToTurnout):
                                #Train 2 will reach the turnout second, so first try to slow that down.
                                if(train2.sprog_speed > 0.5):
                                    #Slow down train 2

                                    # Want to change speed so that train1TimeToTurnout - train2TimeToTurnout > self.TURNOUT_COLLISION_TIME_BUFFER
                                    print("-------------------------------------------------------------TESTING NEW SPROG SPEED----------------------")
                                    print("Train 2 slowing down?")
                                    speed_steps = train2.getSpeedStepsArray()
                                    print("Speed steps: " + str(speed_steps))
                                    curr_test_sprog_speed = train2.sprog_speed
                                    print("Current train sprog speed: " + str(curr_test_sprog_speed))
                                    speed_change_good = False
                                    new_speed_max = train2Dist / (self.TURNOUT_COLLISION_TIME_BUFFER + train1TimeToTurnout)
                                    print("New max speed we need: " + str(new_speed_max))
                                    while(curr_test_sprog_speed > 0.5 and speed_change_good == False):
                                        curr_test_sprog_speed -= 0.2
                                        print("Current testing sprog speed: " + str(curr_test_sprog_speed))
                                        new_approx_speed = speed_steps[int(curr_test_sprog_speed*10)]
                                        print("New approximate speed: " + str(new_approx_speed))
                                        if(new_approx_speed < new_speed_max):
                                            speed_change_good = True
                                    change_in_sprog_speed = curr_test_sprog_speed - train2.sprog_speed
                                    print("Calculated change in sprog speed: " + str(change_in_sprog_speed))
                                    print("---------------------------------------------------------END TESTING NEW SPROG SPEED----------------------")
                                    
                                    self.changeTrainSpeed(train2,change_in_sprog_speed)
                                    return # Stop looking for collisions, fix is in place
                                elif(train1.sprog_speed < 0.9):
                                    # Speed up train 1

                                    print("-------------------------------------------------------------TESTING NEW SPROG SPEED----------------------")
                                    print("Train 1 speeding up?")
                                    speed_steps = train1.getSpeedStepsArray()
                                    print("Speed steps: " + str(speed_steps))
                                    curr_test_sprog_speed = train1.sprog_speed
                                    print("Current train sprog speed: " + str(curr_test_sprog_speed))
                                    speed_change_good = False
                                    new_speed_min = train1Dist / (train2TimeToTurnout - self.TURNOUT_COLLISION_TIME_BUFFER)
                                    while(curr_test_sprog_speed < 0.9 and speed_change_good == False):
                                        curr_test_sprog_speed += 0.2
                                        print("Current testing sprog speed: " + str(curr_test_sprog_speed))
                                        new_approx_speed = speed_steps[int(curr_test_sprog_speed*10)]
                                        print("New approximate speed: " + str(new_approx_speed))
                                        if(new_approx_speed > new_speed_min):
                                            speed_change_good = True
                                    change_in_sprog_speed = curr_test_sprog_speed - train1.sprog_speed
                                    print("Calculated change in sprog speed: " + str(change_in_sprog_speed))
                                    print("---------------------------------------------------------END TESTING NEW SPROG SPEED----------------------")

                                    self.changeTrainSpeed(train1,0.2)
                                    return # Stop looking for collisions, fix is in place
                                else:
                                    #This option means that train 2 cannot slow down, and train 1 cannot speed up
                                    # FIGURE OUT WHAT TO DO HERE
                                    print("CASE 3 FIX ME!")
                                    return # Stop looking for collisions, fix is in place

                        
                    



    def oppositeDirectionCollisionChecks(self, frontArray, backArray, checkTrain):
        #Check to see if other train is ahead or behind train, and use this to perform checks
        trainInFront = False
        trainInBack = False
        otherTrain = None
        otherTrainDist = None
        for distTuple in frontArray:
            if isinstance(distTuple[0], Train):
                otherTrain = distTuple[0]
                otherTrainDist = distTuple[1]
                trainInFront = True
        for distTuple in backArray:
            if isinstance(distTuple[0], Train):
                otherTrain = distTuple[0]
                otherTrainDist = distTuple[1]
                trainInBack = True                                                                                                                                                                                                                                          


    def processBlockForTrainCCW(self, block, checkDist, currentDist):
        returnArray = []
        if block != None:
            for train in self.trains:
                if train.current_block == block and train.distance_in_block < checkDist:
                    returnArray.append((train, currentDist+train.distance_in_block))
            if checkDist > block.distance:
                checkDist -= block.distance
                currentDist += block.distance
                temp = self.processBlockForTrainCCW(block.right_block_straight, checkDist, currentDist)
                returnArray.extend(temp)
                if block.turnout_right != None:
                    temp = self.processBlockForTrainCCW(block.right_block_turn, checkDist, currentDist)
                    returnArray.extend(temp)
        return returnArray


    def processBlockForTrainCW(self, block, checkDist, currentDist):
        returnArray = []
        if block != None:
            for train in self.trains:
                if train.current_block == block and block.distance-train.distance_in_block < checkDist:
                    returnArray.append((train, currentDist+block.distance-train.distance_in_block))
            if checkDist > block.distance:
                checkDist -= block.distance
                currentDist += block.distance
                temp = self.processBlockForTrainCW(block.left_block_straight, checkDist, currentDist)
                returnArray.extend(temp)
                if block.turnout_left != None:
                    temp = self.processBlockForTrainCW(block.left_block_turn, checkDist, currentDist)
                    returnArray.extend(temp)
        return returnArray

    # Function to change the speed of a train, including updating the train
    #  before changing speed
    def changeTrainSpeed(self, train, sprog_speed_change):
        ## DELETE ME (NEXT 2 LINES)
        if train.sprog_speed == 1.0 and sprog_speed_change == -0.2:
            sprog_speed_change = -0.4
        new_speed = train.sprog_speed + sprog_speed_change
        os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py " + str(train.train_id) + " " + str(new_speed))
        print("Changing the speed of " + str(train.train_id) + " to " + str(new_speed) + " from " + str(train.sprog_speed))
        train.updateTrain(datetime.datetime.utcnow())
        change_time = train.setNewSPROGSpeed(new_speed)
        self.fix_time_remaining = change_time + self.FIX_TIME_BUFFER
        print("Calculated fix time: " + str(self.fix_time_remaining))
        self.time_of_last_check = datetime.datetime.utcnow()
        
        

    def breakerActivated(self, breaker, time_of_break):
        print("Activated: " + str(breaker.breaker_id))

##        if(breaker.breaker_id == 8 and self.trains[0].speed_slots_count > 5):
##            new_speed = 0.0
##            if(self.state == 0):
##                new_speed = 0.4
##                self.state = 1
##            elif(self.state == 1):
##                new_speed = 1.0
##                self.state = 2
##            elif(self.state == 2):
##                new_speed = 0.2
##                self.state = 0
##            os.system("python /home/pi/teamge/user/Matt/changeSpeedOfficial.py 1 " + str(new_speed))
##            self.trains[0].updateTrain(datetime.datetime.utcnow())
##            self.trains[0].setNewSPROGSpeed(new_speed)

        #Code for on activation
        #See if trains are all initialized
        initialized = True
        for train in self.trains:
            if train.initialized == False:
                initialized = False
                break
        if(initialized == False):
            available_trains = []
            for train in self.trains:
                if(train.current_segment == breaker.left_segment or train.current_segment == breaker.right_segment):
                    if(train.initialized == False and train.last_breaker_hit !=  breaker):
                        available_trains.append(train)
            if(len(available_trains)==1):
                if(available_trains[0].last_breaker_hit == None):
                    print("Initialize 1")
                    #Calculate direction
                    available_trains[0].last_breaker_hit = breaker.breaker_id
                    available_trains[0].time_of_last_hit = time_of_break
                    if(available_trains[0].current_segment == breaker.left_segment):
                        print("C-Clockwise")
                        print("B" + str(breaker.right_segment))
                        available_trains[0].direction = "counter-clockwise"
                        available_trains[0].current_segment = breaker.right_segment
                    elif(available_trains[0].current_segment == breaker.right_segment):
                        print("Clockwise")
                        available_trains[0].direction = "clockwise"
                        print("B" + str(breaker.left_segment))
                        available_trains[0].current_segment = breaker.left_segment
                elif(available_trains[0].last_breaker_hit != None and available_trains[0].speed == None):
                    print("Initialize 2")
                    #Calculate speed
                    distance = 0
                    temp = None
                    # Determine Pair based on direction
                    if(available_trains[0].direction == "counter-clockwise"):
                        temp = Pair(available_trains[0].last_breaker_hit,breaker.breaker_id,0)
                    elif(available_trains[0].direction == "clockwise"):
                        temp = Pair(breaker.breaker_id,available_trains[0].last_breaker_hit,0)
                    for pair in self.pairs:
                        if(pair.compare(temp)):
                            distance = pair.distance
                            break
                    available_trains[0].setSpeedForAverage(distance/((time_of_break-available_trains[0].time_of_last_hit).total_seconds()))
                    #available_trains[0].speed = distance/((time_of_break-available_trains[0].time_of_last_hit).total_seconds())
                    if(available_trains[0].direction == "clockwise"):
                        available_trains[0].speed *= (-1)
                    print(available_trains[0].speed)
                    # Calculate block, beam breakers are all at distance 0 in their respective block
                    available_trains[0].current_block = breaker.block
                    available_trains[0].distance_in_block = 0
                    #Set as initialized
                    available_trains[0].initialized = True
                    # Set last hit breaker and time
                    available_trains[0].last_breaker_hit = breaker.breaker_id
                    available_trains[0].time_of_last_hit = time_of_break
                    # Set time so can start updating
                    available_trains[0].last_update_time = datetime.datetime.utcnow()
        #After if block

        #Check for trains in neighboring blocks
        self.updateTrains()


        trainArray = []
        trainArray.extend(self.processBlockForTrainCCW(breaker.block, self.TRAIN_CHECK_DIST, 0))
        trainArray.extend(self.processBlockForTrainCW(breaker.block.left_block_straight, self.TRAIN_CHECK_DIST, 0))
        print(trainArray)

        train_to_update = None
        train_distance = None
        for trainTuple in trainArray:
            if train_to_update == None:
                train_to_update = trainTuple[0]
                train_distance = trainTuple[1]
            else:
                if trainTuple[1] < train_distance:
                    train_to_update = trainTuple[0]
                    train_distance = trainTuple[1]

        if train_to_update == None:
            #if(initialized == True):
                #os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py")
            print("--------------------------------------------------------------------NO TRAIN COULD HAVE SET THIS OFF!!")
        else:
            #Update the train that was selected for update
            #os.system("sudo python /home/pi/teamge/user/Matt/setGreen.py")
            print("Checking train: " + str(train_to_update.train_id))
            if((time_of_break-train_to_update.time_of_last_hit).total_seconds()!=0.0):
                print("Inside first check")
                print("Train block: " + str(train_to_update.current_block.block_id) + " Breaker Block: " + str(breaker.block.block_id))
                print("Distance: " + str(train_distance))
                print("Updating Train!")
                #Update speed and block distance
                pair_distance = 0
                temp = None
                # Determine Pair based on direction
                if(train_to_update.direction == "counter-clockwise"):
                    temp = Pair(train_to_update.last_breaker_hit,breaker.breaker_id,0)
                elif(train_to_update.direction == "clockwise"):
                    temp = Pair(breaker.breaker_id,train_to_update.last_breaker_hit,0)
                for pair in self.pairs:
                    if(pair.compare(temp)):
                        pair_distance = pair.distance
                        break
                if(pair_distance == 0):
                    print("---------------------------------------------------------------------PAIR DISTANCE IS ZERO--------" + str(train_to_update.last_breaker_hit) + str(breaker.breaker_id))
                print("Pair Distance: " + str(pair_distance))
                print("Time: " + str(((time_of_break-train_to_update.time_of_last_hit).total_seconds())))
                if(train_to_update.last_breaker_hit != breaker.breaker_id and train_to_update.changing_speed == False and train_to_update.restart_beam_breaker_hit == False):
                    train_to_update.setSpeedForAverage(pair_distance/((time_of_break-train_to_update.time_of_last_hit).total_seconds()))
                    #train.speed = pair_distance/((time_of_break-train.time_of_last_hit).total_seconds())
                    if(train_to_update.direction == "clockwise"):
                        train_to_update.speed *= (-1)
                    print("Speed: " + str(train_to_update.speed))
                elif(train_to_update.changing_speed == False and train_to_update.restart_beam_breaker_hit == True):
                    train_to_update.restart_beam_breaker_hit = False
                train_to_update.distance_in_block = 0
                train_to_update.current_block = breaker.block
                #Update last breaker hit and time of hit and update
                train_to_update.last_breaker_hit = breaker.breaker_id
                train_to_update.time_of_last_hit = time_of_break
                train_to_update.last_update_time = time_of_break

        print(" ")
                

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

    def getRight(self):
        if(self.turnout_right == None):
            return self.right_block_straight
        else:
            if(self.turnout_right.current_state == "straight"):
                return self.right_block_straight
            else:
                return self.right_block_turn

    def getLeft(self):
        if(self.turnout_left == None):
            return self.left_block_straight
        else:
            if(self.turnout_left.current_state == "straight"):
                return self.left_block_straight
            else:
                return self.left_block_turn

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
    # num_1 is first and num_2 is second going counter clockwise
    def __init__(self, num_1, num_2, distance):
        self.GPIO1 = num_1
        self.GPIO2 = num_2
        self.distance = distance

    def compare(self, pair):
        if(self.GPIO1 == pair.GPIO1 and self.GPIO2 == pair.GPIO2):
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
        self.num_speed_data_points = 0
        self.direction = None
        self.initialized = False
        self.last_update_time = None
        self.sprog_speed = None

        #Variables for when slowing down and speeding up
        self.CHANGE_RATE = 8
        self.LAG_TIME = 1.5
        self.remaining_lag_time = 0
        self.remaining_change_time = 0
        self.changing_speed = False
        self.speeding_up = None
        self.restart_beam_breaker_hit = False # DELETE ME I AM UNNECESSARY!

        #number of slots in the array of speeds for the train
        self.speed_slots = 10
        self.speed_slots_count = 0
        self.speed_array = []
        self.sprog_speed_steps_array_1_wheels = [0,.5,5.140,8.965,11.571,13.189,14.286,15.291,16.144,16.821,17.357]
        self.sprog_speed_steps_array_3 = [0,.4817,6.4,9.81,12.42,13.99,14.7,15.99,16.78,17.355,17.75]

    def updateTrain(self, time_of_update):
        elapsed_time = (time_of_update - self.last_update_time).total_seconds()
        print("Elapsed update time: " + str(elapsed_time))
        if(self.changing_speed == False):
            print("Updating train as normal")
            if(elapsed_time > 0):
                distance_since_last = self.speed*elapsed_time
                #print(distance_since_last)
                new_dist = self.distance_in_block + distance_since_last
                #print(new_dist)
                do_again = True
                while do_again:
                    do_again = False
                    if(new_dist > self.current_block.distance):
                        new_dist -= self.current_block.distance
                        self.current_block = self.current_block.getRight()
                        do_again = True
                    elif(new_dist < 0):
                        self.current_block = self.current_block.getLeft()
                        new_dist += self.current_block.distance
                        do_again = True
                self.distance_in_block = new_dist
                self.last_update_time = time_of_update
            else:
                #os.system("sudo python /home/pi/teamge/user/Matt/setYellow.py")
                print("Negative elapsed time???")
        else:
            print("Updating train as changing speed")
            if(elapsed_time < self.remaining_lag_time):
                print("IN LAG TIME")
                print("Elapsed time: " + str(elapsed_time))
                distance_since_last = self.speed*elapsed_time
                #print(distance_since_last)
                new_dist = self.distance_in_block + distance_since_last
                #print(new_dist)
                do_again = True
                while do_again:
                    do_again = False
                    if(new_dist > self.current_block.distance):
                        new_dist -= self.current_block.distance
                        self.current_block = self.current_block.getRight()
                        do_again = True
                    elif(new_dist < 0):
                        self.current_block = self.current_block.getLeft()
                        new_dist += self.current_block.distance
                        do_again = True
                self.distance_in_block = new_dist
                self.last_update_time = time_of_update
                self.remaining_lag_time -= elapsed_time
                print("Remaining lag time: " + str(self.remaining_lag_time))
                print("Last update time: " + str(self.last_update_time))
                print("Remaining change time: " + str(self.remaining_change_time))
            elif(elapsed_time > self.remaining_lag_time and elapsed_time < self.remaining_lag_time+self.remaining_change_time):
                print("ABOVE LAG TIME BELOW FINAL")
                if(self.speeding_up == False):
                    distance_since_last = abs(self.speed)*self.remaining_lag_time + (1.0/2.0)*(elapsed_time-self.remaining_lag_time)**2*self.CHANGE_RATE+(abs(self.speed)-self.CHANGE_RATE*(elapsed_time-self.remaining_lag_time))*(elapsed_time-self.remaining_lag_time)
                elif(self.speeding_up == True):
                    distance_since_last = abs(self.speed)*self.remaining_lag_time + (1.0/2.0)*(elapsed_time-self.remaining_lag_time)**2*self.CHANGE_RATE+abs(self.speed)*(elapsed_time-self.remaining_lag_time)
                else:
                    print("FREAK OUT!")
                if(self.direction == "clockwise"):
                    #Make distance covered negative
                    distance_since_last *= -1
                #print(distance_since_last)
                new_dist = self.distance_in_block + distance_since_last
                #print(new_dist)
                do_again = True
                while do_again:
                    do_again = False
                    if(new_dist > self.current_block.distance):
                        new_dist -= self.current_block.distance
                        self.current_block = self.current_block.getRight()
                        do_again = True
                    elif(new_dist < 0):
                        self.current_block = self.current_block.getLeft()
                        new_dist += self.current_block.distance
                        do_again = True
                self.distance_in_block = new_dist
                self.last_update_time = time_of_update

                print("Old speed: " + str(self.speed))
                if(self.speeding_up == False):
                    self.speed = (abs(self.speed)-self.CHANGE_RATE*(elapsed_time-self.remaining_lag_time))
                elif(self.speeding_up == True):
                    self.speed = (abs(self.speed)+self.CHANGE_RATE*(elapsed_time-self.remaining_lag_time))
                if(self.direction == "clockwise"):
                    #Make speed negative
                    self.speed *= -1
                print("New derived speed: " + str(self.speed))
                self.remaining_change_time -= elapsed_time-self.remaining_lag_time
                self.remaining_lag_time = 0
                print("Remaining lag time: " + str(self.remaining_lag_time))
                print("Last update time: " + str(self.last_update_time))
                print("Remaining change time: " + str(self.remaining_change_time))
            elif(elapsed_time > self.remaining_lag_time + self.remaining_change_time):
                print("ABOVE FINAL")
                if(self.speeding_up == False):
                    distance_since_last = abs(self.speed)*self.remaining_lag_time+(1.0/2.0)*(self.remaining_change_time)**2*self.CHANGE_RATE+(abs(self.speed)-self.CHANGE_RATE*(self.remaining_change_time))*(self.remaining_change_time)+(elapsed_time-(self.remaining_lag_time+self.remaining_change_time))*(abs(self.speed)-self.CHANGE_RATE*(self.remaining_change_time))
                elif(self.speeding_up == True):
                    distance_since_last = abs(self.speed)*self.remaining_lag_time+(1.0/2.0)*(self.remaining_change_time)**2*self.CHANGE_RATE+abs(self.speed)*(self.remaining_change_time)+(elapsed_time-(self.remaining_lag_time+self.remaining_change_time))*(abs(self.speed)+self.CHANGE_RATE*(self.remaining_change_time))
                else:
                    print("FREAK OUT!")
                if(self.direction == "clockwise"):
                    #Make distance covered negative
                    distance_since_last *= -1
                #print(distance_since_last)
                new_dist = self.distance_in_block + distance_since_last
                #print(new_dist)
                do_again = True
                while do_again:
                    do_again = False
                    if(new_dist > self.current_block.distance):
                        new_dist -= self.current_block.distance
                        self.current_block = self.current_block.getRight()
                        do_again = True
                    elif(new_dist < 0):
                        self.current_block = self.current_block.getLeft()
                        new_dist += self.current_block.distance
                        do_again = True
                self.distance_in_block = new_dist
                self.last_update_time = time_of_update

                self.speed_slots_count = 0
                self.speed_array = []
                if(self.sprog_speed != 0.0):
                    if(self.speeding_up == False):
                        self.setSpeedForAverage((abs(self.speed)-self.CHANGE_RATE*(self.remaining_change_time)))
                    elif(self.speeding_up == True):
                        self.setSpeedForAverage((abs(self.speed)+self.CHANGE_RATE*(self.remaining_change_time)))
                else:
                    self.setSpeedForAverage(0.0)
                if(self.direction == "clockwise"):
                    #Make speed negative
                    self.speed *= -1
                self.remaining_change_time = 0
                self.remaining_lag_time = 0
                self.changing_speed = False
                print("Remaining lag time: " + str(self.remaining_lag_time))
                print("Last update time: " + str(self.last_update_time))
                print("Remaining change time: " + str(self.remaining_change_time))

    # Set the new sprog speed for the train and prepare for the change in speed
    #  Also return the remaining lag time + remaining change time for collision checking purporses
    def setNewSPROGSpeed(self, sprog_speed):
        #Only change if the new sprog speed is different
        if(sprog_speed != self.sprog_speed):
            print("SETTING SPROG SPEED --------------------------------------------------------------------SPEED------------------")
            if(self.sprog_speed > sprog_speed):
                #We are slowing down
                self.speeding_up = False
            else:
                self.speeding_up = True
            self.sprog_speed = sprog_speed
            self.remaining_lag_time = self.LAG_TIME
##            if(self.train_id == 1):
##                calculated_new_speed = self.sprog_speed_steps_array_1_wheels[int(sprog_speed*10)]
##            elif(self.train_id == 3):
##                calculated_new_speed = self.sprog_speed_steps_array_3[int(sprog_speed*10)]
            calculated_new_speed = (self.getSpeedStepsArray())[int(sprog_speed*10)]
            #calculated_new_speed = 0.0
            #if(sprog_speed != 0.0):
                #calculated_new_speed = 46.9638*(sprog_speed)**4 - 87.7101*(sprog_speed)**3 + 28.4170*(sprog_speed)**2 + 30.1290*(sprog_speed)-.0226
            print("Calculated new seed: " + str(calculated_new_speed))
            speed_diff = abs(abs(self.speed)-calculated_new_speed)
            #self.sprog_speed = sprog_speed
            print("Speed diff: " + str(speed_diff))
            self.remaining_change_time = speed_diff/self.CHANGE_RATE
            self.changing_speed = True
            self.restart_beam_breaker_hit = True
            return self.remaining_lag_time + self.remaining_change_time

    def setSpeedForAverage(self, speed):

        if len(self.speed_array) < self.speed_slots:
            self.speed_array.append(speed)
        else:
            self.speed_array[self.speed_slots_count] = speed
            self.speed_slots_count = (self.speed_slots_count+1) % self.speed_slots
        #Set speed to absolute value for calculations, program above will
        #  change it back to negative if clockwise
        self.speed = abs(sum(self.speed_array)/float(len(self.speed_array)))
        print("Speed array: " + str(self.speed_array))

    def getSpeedStepsArray(self):
        if(self.train_id == 1):
            return self.sprog_speed_steps_array_1_wheels
        elif(self.train_id == 3):
            return self.sprog_speed_steps_array_3


    def __str__(self):
        return "Train: " + str(self.train_id)

    def __repr__(self):
        return "Train: " + str(self.train_id)

# Class for controlling turnouts
class Turnout:
    # Constructor
    def __init__(self, turnout_id, straight_pin_num, turn_pin_num, orientation):
        self.turnout_id = turnout_id
        self.straight_pin_num = straight_pin_num
        self.turn_pin_num = turn_pin_num
        self.current_state = "straight"
        self.pi2IP = "35.9.22.241"
        self.orientation = orientation
        self.block = None
        self.distance_in_block = None

        # Send signal to make physical turnout to straight
        #time.sleep(2)
        self.__activateRelay(self.straight_pin_num)

    def __str__(self):
        return "Turnout: " + str(self.turnout_id)

    def __repr__(self):
        return "Turnout: " + str(self.turnout_id)

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

    # Switch the state of the turnout
    def switchState(self):
        if(self.current_state == "straight"):
            self.activateTurn()
        else:
            self.activateStraight()
            
    # send the signal to activate the correct pin on the pi
    def __activateRelay(self, pin_num):
        #Activate the pin for the duration of the time delay, then shut off
        print("ACTIVATING TURNOUT --------------------------------------------------------------------TURNOUT----------------")
        os.system("python /home/pi/teamge/user/josh/CommunicationSendTest.py " + self.pi2IP + " " + str(pin_num))

    # set the block and distance in block for the turnout
    def setBlock(self, block, dist_in_block):
        self.block = block
        self.distance_in_block = dist_in_block


# Main Program

#Set up the input arguments
train1_segment = 0
train2_segment = 0
if(len(sys.argv) == 2):
    train1_segment = sys.argv[1]
if(len(sys.argv) >= 3):
    train1_segment = sys.argv[1]
    train2_segment = sys.argv[2]
layout=TrainLayout(int(train1_segment),int(train2_segment))
print("started")
output = " "
ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1, timeout=1)

while True:
    try:
        while output != "":
            output = ser.readline()
            if output.strip() != "":
                #print output.strip()
                beam_break = int(output.strip())
                #print beam_break
                #Call activated here!
                layout.activateBreaker(beam_break)
        #Update trains here!
        output = " "
        layout.updateTrains()
    except KeyboardInterrupt:
        print(" Ending program")
        os.system("python /home/pi/teamge/user/Matt/turnTrackOffOfficial.py")
        sys.exit()
