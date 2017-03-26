
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set GPIO25 as input (button)  
trackloop = 0              # initialize global variable for track count
lstart = time.time()

#this function runs after the beam break, and increments loop counter
def beamFunction(channel):
    global trackloop
    global lstart 
    elapsed = (time.time() - lstart )
    print('hello!!!!!!!-3')
    if elapsed > 2:
        print('hello!!!!!!!-2')
        trackloop = trackloop + 1
        print("beam-break triggered. Loop: {} at {}. Elapsed: {}".format(trackloop, time.ctime(), elapsed ))
        lstart = time.time()

#trigger event setup
GPIO.add_event_detect(18, GPIO.FALLING, callback=beamFunction, bouncetime=200)


#main loop  
try:
    print('hello!!!!!!!-1')
    while True:            # this will carry on until you hit CTRL+C  
        print("Waiting for beam break. port status: {}".format(GPIO.input(3)))
        time.sleep(0.1)         # wait 0.1 seconds
  
finally:                   # this block will run no matter how the try block exits  
    print('hello!!!!!!!')
    GPIO.cleanup()         # clean up after yourself
