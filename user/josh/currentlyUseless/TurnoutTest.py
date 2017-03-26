from Turnout import Turnout
import time

test=Turnout(1,16,18)

test.activateTurn()
time.sleep(5)
test.activateStraight()
time.sleep(5)
test.activateStraight()
