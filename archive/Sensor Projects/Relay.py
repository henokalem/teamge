import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class activateRelay():
    def __init__(self):
        #pinList = [26, 19, 13, 6, 5, 21, 20, 16, 17, 25]

        w, h = 2, 5
        self.Matrix = [[0 for x in range(w)] for y in range(h)] 

        self.Matrix[0][0] = 26
        self.Matrix[0][1] = 19
        self.Matrix[1][0] = 13
        self.Matrix[1][1] = 6
        self.Matrix[2][0] = 21
        self.Matrix[2][1] = 5
        self.Matrix[3][0] = 16
        self.Matrix[3][1] = 20
        self.Matrix[4][0] = 17
        self.Matrix[4][1] = 25

        for x in range(0, h):
            for y in range(0, w):
                GPIO.setup(self.Matrix[x][y], GPIO.OUT)
                GPIO.output(self.Matrix[x][y], GPIO.LOW)

    def chgTest(self, x, y, t=0.4):
            GPIO.output(self.Matrix[x][y], GPIO.HIGH)
            print ("pin: " + str(self.Matrix[x][y]), "state: HIGH", time.time())
            time.sleep(t)

            GPIO.output(self.Matrix[x][y], GPIO.LOW)
            print ("pin: %s" % self.Matrix[x][y], "state: LOW-", time.time())
            time.sleep(t)

    def changeTrack(self, s, t=0.4):
            if (s == 0):
                self.chgTest(2,0,t)
                print ("TO3 turned")
            elif (s == 1):
                self.chgTest(0,0,t)
                self.chgTest(2,1,t)
            elif (s == 2):
                self.chgTest(0,1,t)
                self.chgTest(1,1,t)
                self.chgTest(2,1,t)
            else:
                return

    def menuTest(self):
        print("entered menuTest")

        menu = {}
        menu['0']="- TO1 LEFT" 
        menu['1']="- TO1 STRAIGHT" 
        menu['2']="- TO2 LEFT"
        menu['3']="- TO2 STRAIGHT"
        menu['4']="- TO3 LEFT"
        menu['5']="- TO3 STRAIGHT"
        menu['6']="- TO4 LEFT"
        menu['7']="- TO4 STRAIGHT"
        menu['8']="- TO5 LEFT"
        menu['9']="- TO5 STRAIGHT"
        menu['x']="- eXit"

        bExit = True

        while bExit: 
            #options=menu.keys()
            #options=sort()
            options = sorted(menu.keys())
            for entry in options: 
                print (entry, menu[entry])

            selection=input('Please Select:') 
        
            if   selection == '0': 
                self.chgTest(0,0,0.4)
            elif selection == '1': 
                self.chgTest(0,1,0.4)
            elif selection == '2': 
                self.chgTest(1,0,0.4)
            elif selection == '3':
                self.chgTest(1,1,0.4)
            elif selection == '4': 
                self.chgTest(2,0,0.4)
            elif selection == '5': 
                self.chgTest(2,1,0.4)
            elif selection == '6': 
                self.chgTest(3,0,0.4)
            elif selection == '7': 
                self.chgTest(3,1,0.4)
            elif selection == '8': 
                self.chgTest(4,0,0.4)
            elif selection == '9': 
                self.chgTest(4,1,0.4)
            elif selection == 'x': 
                #GPIO.cleanup()
                bExit = False;
                break
            else: 
                print ("Unknown Option Selected!")

        return
