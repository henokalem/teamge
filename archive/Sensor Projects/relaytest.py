import Relay
import data2TimeSeries
import RPi.GPIO as GPIO

clsRelay = Relay.activateRelay()

GPIO.setwarnings(False)

clsRelay.menuTest()


