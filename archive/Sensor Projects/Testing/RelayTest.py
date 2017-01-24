
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#pinlist = [26, 19, 13, 6, 5, 21, 20, 16, 17, 25]

w = 2
h = 5

Matrix = [[0 for x in range(w)] for y in range(h)] 

Matrix[0][0] = 26
Matrix[0][1] = 19
Matrix[1][0] = 13
Matrix[1][1] = 6
Matrix[2][0] = 5
Matrix[2][1] = 21
Matrix[3][0] = 20
Matrix[3][1] = 16
Matrix[4][0] = 17
Matrix[4][1] = 25

for x in range(0, h):
    for y in range(0, w):
		GPIO.setup(Matrix[x][y], GPIO.OUT)
		GPIO.output(Matrix[x][y], GPIO.LOW)


def chgTest(x, y, t=0.4):
	GPIO.output(Matrix[x][y], GPIO.HIGH)
	print("pin: " + str(Matrix[x][y]), "state: HIGH", time.time())
	time.sleep(t)

	GPIO.output(Matrix[x][y], GPIO.LOW)
	print("pin: %s" % Matrix[x][y], "state: LOW-", time.time())

def menuTest():
	print("entered menuTest")

	menu = {}
	menu['1'] = "- TO1 Left"
	menu['2'] = "- TO1 Straight"
	menu['3'] = "- TO2 Left"
	menu['4'] = "- TO2 Straight"
	menu['5'] = "- TO3 Left"
	menu['6'] = "- TO3 Straight"
	menu['7'] = "- TO4 Left"
	menu['8'] = "- TO4 Straight"
	menu['9'] = "- TO5 Left"
	menu['0'] = "- TO5 Straight"

	exit = True
        
        options = sorted(menu.keys())
        for entry in options:
            print (entry, menu[entry])

        while(exit):

		selection = input('Please Select')

		if selection == 1:
			chgTest(0,0,0.4)
		elif selection == 2:
			chgTest(0,1,0.4)
		elif selection == 3:
			chgTest(1,0,0.4)
		elif selection == 4:
			chgTest(1,1,0.4)
		elif selection == 5:
			chgTest(2,0,0.4)
		elif selection == 6:
			chgTest(2,1,0.4)
		elif selection == 7:
			chgTest(3,0,0.4)
		elif selection == 8:
			chgTest(3,1,0.4)
		elif selection == 9:
			chgTest(4,0,0.4)
                elif selection == 0:
			chgTest(4,1,0.4)
                elif selection == x:
			exit = False
			break
		else:
			print("Unknown Key!")

	return

if __name__ == '__main__':     # Program start from here

	try:
		menuTest()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                GPIO.cleanup()
                sys.exit()
