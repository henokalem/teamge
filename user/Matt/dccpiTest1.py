from dccpi import *
import time
e = DCCRPiEncoder()
controller = DCCController(e)  # Create the DCC controller with the RPi encoder
l1 = DCCLocomotive("DCC1", 1)  # Create locos, args: Name, DCC Address (see DCCLocomotive class)

controller.register(l1)        # Register locos on the controller
controller.start()             # Start the controller. Removes brake signal
l1.reverse()                   # Change direction bit

l1.speed = 0                  # Change speed
time.sleep(2)
l1.speed = 10
time.sleep(2)
l1.speed = 0


controller                     # Print info from all locos registered


controller.stop()              # IMPORTANT! Stop controller always. Emergency-stops
