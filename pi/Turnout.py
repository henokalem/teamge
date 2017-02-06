import RPi.GPIO as GPIO
import time

# Class for controlling
class Turnout:
    # Constructor
    def __init__(self, turnout_id, straight_pin_num, turn_pin_num):
        self.turnout_id = turnout_id
        self.straight_pin_num = straight_pin_num
        self.turn_pin_num = turn_pin_num
        self.current_state = "straight"

        # set up the initial GPIO pin outputs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.straight_pin_num, GPIO.OUT)
        GPIO.output(self.straight_pin_num, GPIO.LOW)
        GPIO.setup(self.turn_pin_num, GPIO.OUT)
        GPIO.output(self.turn_pin_num, GPIO.LOW)

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
        GPIO.output(pin_num, GPIO.HIGH)
        print ("pin: " + str(pin_num), "state: HIGH, time: ", time.time())
        time.sleep(time_delay)

        GPIO.output(pin_num, GPIO.LOW)
        print ("pin: " + str(pin_num), "state: LOW, time: ", time.time())
        time.sleep(time_delay) #necessary?
