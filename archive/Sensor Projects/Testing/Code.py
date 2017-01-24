#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import datetime
import smbus
from threading import Timer
import Adafruit_BMP.BMP085 as BMP085
from i2clibraries import i2c_hmc5883l
bmp085 = BMP085.BMP085()
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
BUS = smbus.SMBus(1)

BtnAPin = 12
BtnBPin = 13
BtnCPin = 15
Gpin   = 16
Rpin   = 18

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
        GPIO.setmode(GPIO.BOARD)
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
        Line = 'TempC:'+'{0:0.2f}'.format(bmp085.read_temperature())
        write(0,1,Line)
        print(Line)
        
def Led(x):
	if x == 0:
		GPIO.output(Rpin, 1)
		GPIO.output(Gpin, 0)
	if x == 1:
		GPIO.output(Rpin, 0)
		GPIO.output(Gpin, 1)

def Print(val,chn):
        if val == 0:
                if chn == BtnAPin:
                        print('Button A pressed')
                        write(0,0,'Scenario A')
                elif chn == BtnBPin:
                        print('Button B pressed')
                        write(0,0,'Scenario B')
                elif chn == BtnCPin:
                        print('Button C pressed')
                        write(0,0,'Scenario C')
        
def detect(chn):
	Led(GPIO.input(chn))
	Print(GPIO.input(chn), chn)

def loop():
        counter = 0
        while True:
                counter = counter + 1
                utc = datetime.datetime.utcnow()
                utc = utc.strftime('%m/%d/%Y %H:%M:%S')
                line = utc + ',' + '001,'+('{0:0.2f},'.format(bmp085.read_temperature()))+('{0:0.2f},'.format(bmp085.read_pressure()))+('{0:0.2f},'.format(bmp085.read_altitude()))+('{0:0.2f},{1:0.2f},'.format(hmc5883l.getHeading()[0],hmc5883l.getHeading()[1]))+('{0:0.2f},{1:0.2f},{2:0.2f}'.format(hmc5883l.getAxes()[0],hmc5883l.getAxes()[1],hmc5883l.getAxes()[2]))
                if counter >= 5:
                        counter = 0
                        Line = 'TempC:'+'{0:0.2f}'.format(bmp085.read_temperature())
                        write(0,1,Line)
                        print(Line)
                with open(outFileName, 'a') as output:
                        output.write(line+'\n')
                time.sleep(1)

def destroy():
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

