#!/usr/bin/env python
import sys
import smbus
import time
import datetime
import RPi.GPIO as GPIO
from threading import Timer
from Adafruit_BMP import BMP085
from i2clibraries import i2c_hmc5883l
import Relay
import data2TimeSeries

bmp085   = BMP085.BMP085()
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
BUS      = smbus.SMBus(1)

clsRelay = Relay.activateRelay()
clsSendData = data2TimeSeries.SendData()

GPIO.setwarnings(False)

#BtnAPin = 12
#BtnBPin = 13
#BtnCPin = 15
#Gpin    = 16
#Rpin    = 18
BtnAPin = 18
BtnBPin = 27
BtnCPin = 22
Gpin    = 23
Rpin    = 24

def write_word(addr, data):
	global BLEN
	temp = data
	if BLEN == 1:
		temp |= 0x08
	else:
		temp &= 0xF7
	BUS.write_byte(addr ,temp)

def send_command(comm):
	# Send bit7-4 firstly
	buf = comm & 0xF0
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (comm & 0x0F) << 4
	buf |= 0x04               # RS = 0, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

def send_data(data):
	# Send bit7-4 firstly
	buf = data & 0xF0
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

	# Send bit3-0 secondly
	buf = (data & 0x0F) << 4
	buf |= 0x05               # RS = 1, RW = 0, EN = 1
	write_word(LCD_ADDR ,buf)
	time.sleep(0.002)
	buf &= 0xFB               # Make EN = 0
	write_word(LCD_ADDR ,buf)

def init(addr, bl):
#	global BUS
#	BUS = smbus.SMBus(1)
	global LCD_ADDR
	global BLEN
	LCD_ADDR = addr
	BLEN = bl
	try:
		send_command(0x33) # Must initialize to 8-line mode at first
		time.sleep(0.005)
		send_command(0x32) # Then initialize to 4-line mode
		time.sleep(0.005)
		send_command(0x28) # 2 Lines & 5*7 dots
		time.sleep(0.005)
		send_command(0x0C) # Enable display without cursor
		time.sleep(0.005)
		send_command(0x01) # Clear Screen
		BUS.write_byte(LCD_ADDR, 0x08)
	except:
		return False
	else:
		return True

def clear():
	send_command(0x01) # Clear Screen

def openlight():  # Enable the backlight
	BUS.write_byte(0x27,0x08)
	BUS.close()

def write(x, y, str):
	if x < 0:
		x = 0
	if x > 15:
		x = 15
	if y <0:
		y = 0
	if y > 1:
		y = 1

	# Move cursor
	addr = 0x80 + 0x40 * y + x
	send_command(addr)

	for chr in str:
		send_data(ord(chr))

def setup():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Gpin, GPIO.OUT)
        GPIO.setup(Rpin, GPIO.OUT)
        GPIO.setup(BtnAPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BtnBPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BtnCPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BtnAPin, GPIO.BOTH, callback=detect, bouncetime=200)
        GPIO.add_event_detect(BtnBPin, GPIO.BOTH, callback=detect, bouncetime=200)
        GPIO.add_event_detect(BtnCPin, GPIO.BOTH, callback=detect, bouncetime=200)
        init(0x27,1)
        clear()
        utc = datetime.datetime.utcnow()
        global outFileName, objFile
        outFileName = "/tmp/sensors"+utc.strftime('%m%d%Y')+".csv"
        header = "UTC-Date-Time, SensorID, TempC,PressurePA,AltM,HeadingDeg,HeadingMin,AxX,AxY,AxZ"
        with open(outFileName, 'w') as output:
                output.write(header+'\n')
        hmc5883l.setContinuousMode()
        hmc5883l.setDeclination(0,6)
        Print(0,BtnAPin)
        clsRelay.changeTrack(0, 0.4)    # initialize track to default state
        #Line = 'TempC:'+'{0:0.2f}'.format(bmp085.read_temperature())
        #write(0,1,Line)
        #print(Line)
        
def Led(x):
    #print ("led x: ", x)
    if x == BtnAPin:
        GPIO.output(Rpin, GPIO.HIGH)
        GPIO.output(Gpin, GPIO.LOW)
    elif x == BtnBPin:
        GPIO.output(Rpin, GPIO.LOW)
        GPIO.output(Gpin, GPIO.HIGH)
    elif x == BtnCPin:
        GPIO.output(Rpin, GPIO.LOW)
        GPIO.output(Gpin, GPIO.LOW)

def Print(val,chn):
        global clsRelay
        if val == 0:
                if chn == BtnAPin:
                        print('Button A pressed')
                        write(0,0,'Scenario A')
                        clsRelay.changeTrack(0, 0.4)
                elif chn == BtnBPin:
                        print('Button B pressed')
                        write(0,0,'Scenario B')
                        clsRelay.changeTrack(1, 0.4)
                elif chn == BtnCPin:
                        print('Button C pressed')
                        write(0,0,'Scenario C')
                        #clsRelay.menuTest()
                        clsRelay.changeTrack(2, 0.4)
        
def detect(chn):
	Led(chn)
	Print(GPIO.input(chn), chn)

def loop():
        counter = 0
        while True:
                counter = counter + 1
                utc = datetime.datetime.utcnow()
                utc = utc.strftime('%m/%d/%Y %H:%M:%S')
                #line = utc + ',' + '001,'+('{0:0.2f},'.format(bmp085.read_temperature()))+('{0:0.2f},'.format(bmp085.read_pressure()))+('{0:0.2f},'.format(bmp085.read_altitude()))+('{0:0.2f},{1:0.2f},'.format(hmc5883l.getHeading()[0],hmc5883l.getHeading()[1]))+('{0:0.2f},{1:0.2f},{2:0.2f}'.format(hmc5883l.getAxes()[0],hmc5883l.getAxes()[1],hmc5883l.getAxes()[2]))
                line = utc + ',001,'+('{0:0.2f},'.format(bmp085.read_pressure()))+('{0:0.2f}'.format(bmp085.read_temperature()))
                if counter >= 5:
                        counter = 0
                        Line = 'TempC:'+'{0:0.2f}'.format(bmp085.read_temperature())
                        write(0,1,Line)
                        print(line)
                        # orig output: 07/29/2016 16:10:59,001,21.80,99141.00,182.93,11.00,39.00,297.16,60.72,393.76
                        # new output: 
                        #fieldnames      = ("datetime","sensorid","humidity","temperature")
                        clsSendData.formatAndSendData(line)
                with open(outFileName, 'a') as output:
                        output.write(line+'\n')
                time.sleep(1)

def destroy():
        global Gpin, Rpin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Gpin, GPIO.OUT)
        GPIO.setup(Rpin, GPIO.OUT)
        GPIO.output(Gpin, GPIO.HIGH)       # Green led off
        GPIO.output(Rpin, GPIO.HIGH)       # Red led off
        GPIO.cleanup()                     # Release resource
        clear()

if __name__ == '__main__':     # Program start from here
	setup()

	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                destroy()
                sys.exit()

