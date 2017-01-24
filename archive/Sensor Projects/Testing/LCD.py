import sys
import smbus
import time
import datetime
import RPi.GPIO as GPIO
from threading import Timer

BUS = smbus.SMBus(1)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def write_word(addr, data):
	global BLEN
	temp = data
	if BLEN == 1:
		temp |= 0x08
	else:
		temp &= 0xF7
	BUS.write_byte(addr, temp)

def send_command(comm):
	# Send bit7-4 firstly
	buf = comm & 0xF0
	buf |= 0x04
	write_word(LCD_ADDR, buf)
	time.sleep(0.002)
	buf &= 0xFB
	write_word(LCD_ADDR, buf)

	# Send bit 3-0 secondly
	buf = (comm & 0x0F) << 4
	buf |= 0x04
	write_word(LCD_ADDR, buf)
	time.sleep(0.002)
	buf &= 0xFB
	write_word(LCD_ADDR, buf)

def send_data(data):
	# Send bit7-4 firstly
	buf = data & 0xF0
	buf |= 0x05
	write_word(LCD_ADDR, buf)
	time.sleep(0.002)
	buf &= 0xFB
	write_word(LCD_ADDR, buf)

def init(addr, bl):
	# global BUS
	# BUS = smbus.SMBus(1)
	global LCD_ADDR
	global BLEN
	LCD_ADDR = addr
	BLEN = bl
	try:
		send_command(0x33) # Must initialize to 8 line mode at first
		time.sleep(0.005)
		send_command(0x32) # Then initialize to 4 line mode
		time.sleep(0.005)
		send_command(0x28)
		time.sleep(0.005)
		send_command(0x0C)
		time.sleep(0.005)
		send_command(0x01)
		BUS.write_byte(LCD_ADDR, 0x08)
	except:
		return False
	else:
		return True

def clear():
	send_command(0x01) # Clear Screen

def openlight(): # Enable the backlight
	BUS.write_byte(0x27, 0x08)
	BUS.close()

def write(x, y, str):
	if x < 0:
		x = 0
	if x > 15:
		x = 15
	if y < 0:
		y = 0
	if y > 1:
		y = 1

	# Move cursor
	addr = 0x80 + 0x40 * y + x
	send_command(addr)

	for chr in str:
		send_data(ord(chr))

def setup():
	init(0x27,1)
	clear()

	counter = 0
	while True:
		counter = counter + 1
                
		write(0,1,'Scenario')

		if counter >= 10:
			break

		time.sleep(1)

if __name__== '__main__':
	
	try:
		setup()
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit





		



