import RPi.GPIO as GPIO, time  

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set GPIO25 as input (button)  
trackloop = 0              # initialize global variable for track count

#this function runs after the beam break, and increments loop counter
def beamFunction(channel):
    global trackloop
    trackloop = trackloop + 1
    print("beamFunction triggered. Loop: {} at {}".format(trackloop, time.ctime()) )

#trigger event setup
GPIO.add_event_detect(12, GPIO.FALLING, callback=beamFunction, bouncetime=200)


#main loop  
try:  
    while True:            # this will carry on until you hit CTRL+C  
#	print("Waiting for beam break. port status: {}".format(GPIO.input(12)) )
        time.sleep(0.1)         # wait 0.1 seconds  
  
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()         # clean up after yourself
