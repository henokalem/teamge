import csv
import time

class Train(object):
    def __init__(self, decoderID, speed, isForward):
        self.decoderID = decoderID
        self.speed = speed
        self.isForward = isForward

class BoolObj(object):
    def __init__(self, boolean):
        self.boolean = boolean
        
trains = []
continueLoop = False
obj = BoolObj(False)

try:
    f = open('/home/pi/teamge/user/josh/trainProperties.txt')
    try:
        reader = csv.reader(f)
        firstRow = True
        for row in reader:
            if(firstRow):
                if(row[0] == "True"):
                    continueLoop = True
                    obj.boolean = True
                elif(row[0] == "False"):
                    continueLoop = False
                    obj.boolean = False
                else:
                    print("error")
                firstRow = False
            else:
                newTrain = Train(int(row[0]),float(row[1]),bool(row[2]))
                trains.append(newTrain)
    finally:
        f.close()
except IOError:
    print("Could not open file")

print continueLoop
for train in trains:
    print str(train.decoderID) + "," + str(train.speed) + "," + str(train.isForward)

while continueLoop:
    time.sleep(0.5)
    try:
        f = open('/home/pi/teamge/user/josh/trainProperties.txt')
        try:
            reader = csv.reader(f)
            firstRow = True
            for row in reader:
                if(firstRow):
                    if(row[0] == "True"):
                        if(continueLoop == False):
                            print("Continue Loop changed to True!")
                            continueLoop = True
                        else:
                            print("No change")
                    elif(row[0] == "False"):
                        if(continueLoop == True):
                            print("Continue Loop Changed to False!")
                            continueLoop = False
                        else:
                            print("No Change")
                    else:
                        print("error")
                    firstRow = False
                else:
                    a = 2
                    #newTrain = Train(int(row[0]),float(row[1]),bool(row[2]))
                    #trains.append(newTrain)
        finally:
            f.close()
    except IOError:
        print("Could not open file")
