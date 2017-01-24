import RPi.GPIO as GPIO
import time
import datetime
import smbus
import Adafruit_BMP.BMP085 as BMP085
from i2clibraries import i2c_hmc5883l
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
bmp085 = BMP085.BMP085()
BUS = smbus.SMBus(1)

def setup():
    utc = datetime.datetime.utcnow()
    global outFileName
    outFileName = "/tmp/sensors"+utc.strftime('%m%d%Y')+".csv"
    header = "UTC-Date-Time, SensorID, TempC,PressurePA,AltM,HeadingDeg,HeadingMin,AxX,AxY,AxZ"
    print(header)
    global objFile
    with open(outFileName, 'w') as output:
        output.write(header+'\n')
    hmc5883l.setContinuousMode()
    hmc5883l.setDeclination(0,6)
    
def destroy():
    print("End.")
    
def loop():
        while True:
                utc = datetime.datetime.utcnow()
                utc = utc.strftime('%m/%d/%Y %H:%M:%S')
                line = utc + ',' + '001,'+('{0:0.2f},'.format(bmp085.read_temperature()))+('{0:0.2f},'.format(bmp085.read_pressure()))+('{0:0.2f},'.format(bmp085.read_altitude()))+('{0:0.2f},{1:0.2f},'.format(hmc5883l.getHeading()[0],hmc5883l.getHeading()[1]))+('{0:0.2f},{1:0.2f},{2:0.2f}'.format(hmc5883l.getAxes()[0],hmc5883l.getAxes()[1],hmc5883l.getAxes()[2]))
                print(line)
                with open(outFileName, 'a') as output:
                    output.write(line+'\n')
                time.sleep(1)
                
                

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
