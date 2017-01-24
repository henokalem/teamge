import RPi.GPIO as GPIO, time

#For information about the GPIO.steup, check out
#   https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# Channel 12 is the beam break that is glued upside-down in an underpass

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set GPIO25 as input (button)  
trackloop = 0              # initialize global variable for track count
lstart = time.time()

#this function runs after the beam break, and increments loop counter
def beamFunction(channel):
    global trackloop
    global lstart 
    elapsed = (time.time() - lstart )
    if elapsed > 2:
        trackloop = trackloop + 1
        print("beam-break triggered. Loop: {} at {}. Elapsed: {}".format(trackloop, time.ctime(), elapsed ))
        lstart = time.time()    

#trigger event setup
GPIO.add_event_detect(12, GPIO.FALLING, callback=beamFunction, bouncetime=200)


#main loop  
try:  
    while True:            # this will carry on until you hit CTRL+C  
#	print("Waiting for beam break. port status: {}".format(GPIO.input(12)) )
       time.sleep(0.1)         # wait 0.1 seconds  
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself
